#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <cuda_runtime.h>
#include "windows.h"
#include "device_launch_parameters.h"
typedef unsigned char uchar;

float* ReadBMP(const char *bmpName, int *width, int *height)
{
	FILE *fp;
	uchar *img_raw; float *image;
	int bmpwidth, bmpheight, linebyte, npixels, i, j; if ((fp = fopen(bmpName, "rb")) == NULL)
	{
		printf("Failed to open the image.\n");
		return 0;
	} if (fseek(fp, sizeof(BITMAPFILEHEADER), 0))
	{
		printf("Failed to skip the file header.\n");
		return 0;
	} BITMAPINFOHEADER bmpInfoHeader;
	fread(&bmpInfoHeader, sizeof(BITMAPINFOHEADER), 1, fp);
	bmpwidth = bmpInfoHeader.biWidth;
	bmpheight = bmpInfoHeader.biHeight;
	npixels = bmpwidth*bmpheight;
	linebyte = (bmpwidth * 24 / 8 + 3) / 4 * 4; img_raw = (uchar*)malloc(linebyte*bmpheight);
	fread(img_raw, linebyte*bmpheight, 1, fp); image = (float*)malloc(sizeof(float)*npixels);
	for (i = 0; i < bmpheight; i++)
		for (j = 0; j < bmpwidth; j++)
			image[i*bmpwidth + j] = (float)img_raw[i*linebyte + j * 3];
	*width = bmpwidth;
	*height = bmpheight; free(img_raw);
	fclose(fp);
	return image;
}

void MarkAndSave(const char* bmpName, int X1, int Y1, int X2, int Y2, const char* outputBmpName)
{
	FILE *fp;
	uchar *img_raw; float *image;
	BITMAPFILEHEADER bmpFileHeader;
	BITMAPINFOHEADER bmpInfoHeader;
	int bmpwidth, bmpheight, linebyte, npixels;
	if ((fp = fopen(bmpName, "rb")) == NULL)
	{
		printf("Failed to open the original image.\n");
		return;
	} fread(&bmpFileHeader, sizeof(BITMAPFILEHEADER), 1, fp);
	fread(&bmpInfoHeader, sizeof(BITMAPINFOHEADER), 1, fp);
	bmpwidth = bmpInfoHeader.biWidth;
	bmpheight = bmpInfoHeader.biHeight;
	npixels = bmpwidth*bmpheight;
	linebyte = (bmpwidth * 24 / 8 + 3) / 4 * 4; img_raw = (uchar*)malloc(linebyte*bmpheight);
	fread(img_raw, linebyte*bmpheight, 1, fp);
	fclose(fp); if (X1 < 0 || X2 >= bmpwidth || Y1 < 0 || Y2 >= bmpheight)
	{
		printf("Invalid rectangle position!\n");
		return;
	}
	int i;
	for (i = X1; i <= X2; i++)
	{
		img_raw[Y1*linebyte + i * 3] = 0;
		img_raw[Y1*linebyte + i * 3 + 1] = 0;
		img_raw[Y1*linebyte + i * 3 + 2] = 255;
		img_raw[Y2*linebyte + i * 3] = 0;
		img_raw[Y2*linebyte + i * 3 + 1] = 0;
		img_raw[Y2*linebyte + i * 3 + 2] = 255;
	}
	for (i = Y1 + 1; i < Y2; i++)
	{
		img_raw[i*linebyte + X1 * 3] = 0;
		img_raw[i*linebyte + X1 * 3 + 1] = 0;
		img_raw[i*linebyte + X1 * 3 + 2] = 255;
		img_raw[i*linebyte + X2 * 3] = 0;
		img_raw[i*linebyte + X2 * 3 + 1] = 0;
		img_raw[i*linebyte + X2 * 3 + 2] = 255;
	} if ((fp = fopen(outputBmpName, "wb")) == NULL)
	{
		printf("Failed to open the output image.\n");
		return;
	}
	fwrite(&bmpFileHeader, sizeof(BITMAPFILEHEADER), 1, fp);
	fwrite(&bmpInfoHeader, sizeof(BITMAPINFOHEADER), 1, fp);
	fwrite(img_raw, linebyte*bmpheight, 1, fp); free(img_raw);
	fclose(fp);
}

//use to get the Template's data
float* getTemdata(float *tem, float *output, int K) {
	for (int i = 0; i < K*K; i++) {
		output[0] += tem[i] / (K*K);
	}
	for (int i = 0; i < K*K; i++) {
		output[1] += tem[i] * tem[i] / (K*K);
	}
	output[1] = output[1] - output[0] * output[0];

	for (int i = 0; i < K*K; i++) {
		int j = i % K;
		int j_minus_x = j - K / 2;
		output[2] += tem[i] * j_minus_x;
	}
	output[2] = 4 * output[2] / (K*K*K);

	for (int i = 0; i < K*K; i++) {
		int l = i / K;
		int l_minus_y = l - K / 2;
		output[3] += tem[i] * l_minus_y;
	}
	output[3] = 4 * output[3] / (K*K*K); return output;
}

//TO DO: WRITE KERNELS HERE
__global__ void Row_Cumulate_gpu(float *Image, float *L1_dev_row, float *L2_dev_row, float *L3_dev_row, float *L4_dev_row, int m, int n)
{
	int index = blockIdx.x * 128 + threadIdx.x;
	int i, j, k;

	if (index >= n) return;

	L1_dev_row[index * m] = Image[index * m];
	for (j = 1; j < m; j++)
	{
		L1_dev_row[index * m + j] = L1_dev_row[index * m + j - 1] + Image[index * m + j];
	}

	L2_dev_row[index * m] = Image[index * m] * Image[index * m];
	for (j = 1; j < m; j++)
	{
		L2_dev_row[index * m + j] = L2_dev_row[index * m + j - 1] + Image[index * m + j] * Image[index * m + j];
	}

	L3_dev_row[index * m] = Image[index * m] * 0;
	for (j = 1; j < m; j++)
	{
		L3_dev_row[index * m + j] = L3_dev_row[index * m + j - 1] + Image[index * m + j] * (j);
	}

	L4_dev_row[index * m] = Image[index * m] * (index);
	for (j = 1; j < m; j++)
	{
		L4_dev_row[index * m + j] = L4_dev_row[index * m + j - 1] + Image[index * m + j] * (index);
	}
}

__global__ void Column_Cumulate_gpu(float *L1_Row, float *L2_Row, float *L3_Row, float *L4_Row, float *L1, float *L2, float *L3, float *L4, int m, int n)
{
	int index = blockIdx.x * 128 + threadIdx.x;
	int i, j;

	if (index >= m) return;

	L1[index] = L1_Row[index];
	for (j = 1; j < n; j++)
	{
		L1[index + j * m] = L1[index + (j - 1) * m] + L1_Row[index + j * m];
	}

	L2[index] = L2_Row[index];
	for (j = 1; j < n; j++)
	{
		L2[index + j * m] = L2[index + (j - 1) * m] + L2_Row[index + j * m];
	}

	L3[index] = L3_Row[index];
	for (j = 1; j < n; j++)
	{
		L3[index + j * m] = L3[index + (j - 1) * m] + L3_Row[index + j * m];
	}

	L4[index] = L4_Row[index];
	for (j = 1; j < n; j++)
	{
		L4[index + j * m] = L4[index + (j - 1) * m] + L4_Row[index + j * m];
	}
}

__global__ void kernel_3(float *L1_dev, float *L2_dev, float *L3_dev, float *L4_dev, float *output_dev, int N, int M, int L, float *tem_inf)
{
	int row_ID, col_ID;
	float S1, S2, S3, S4, V1, V2, V3, V4;
	int index = blockIdx.x*blockDim.x + threadIdx.x;

	row_ID = index / M;
	col_ID = index % M;

	if (col_ID < (L / 2) || (col_ID >(M - L / 2 - (L % 2 > 0))) || (row_ID > (N - L / 2 - (L % 2 > 0))) || (row_ID < (L / 2))) {
		V1 = 0;
		V2 = 0;
		V3 = 0;
		V4 = 0;
	}

	else {
		if ((col_ID != L / 2) && (row_ID != L / 2)) {
			S1 = L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1] - L1_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] + L1_dev[(row_ID - L / 2 - 1)*M + (col_ID - L / 2 - 1)];
			S2 = L2_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L2_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1] - L2_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] + L2_dev[(row_ID - L / 2 - 1)*M + (col_ID - L / 2 - 1)];
			S3 = L3_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L3_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1] - L3_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] + L3_dev[(row_ID - L / 2 - 1)*M + (col_ID - L / 2 - 1)];
			S4 = L4_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L4_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1] - L4_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] + L4_dev[(row_ID - L / 2 - 1)*M + (col_ID - L / 2 - 1)];
			V1 = S1 / (L*L);
			V2 = S2 / (L*L) - (V1*V1);
			V3 = 4 * (S3 - col_ID*S1) / (L*L*L);
			V4 = 4 * (S4 - row_ID*S1) / (L*L*L);
		}
		else if ((col_ID == L / 2) && (row_ID != L / 2)) {
			S1 = L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L1_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			S2 = L2_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L2_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			S3 = L3_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L3_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			S4 = L4_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L4_dev[(row_ID - L / 2 - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			V1 = S1 / (L*L);
			V2 = S2 / (L*L) - (V1*V1);
			V3 = 4 * (S3 - col_ID*S1) / (L*L*L);
			V4 = 4 * (S4 - row_ID*S1) / (L*L*L);
		}
		else if ((col_ID != L / 2) && (row_ID == L / 2)) {
			S1 = L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1];
			S2 = L2_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1];
			S3 = L3_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1];
			S4 = L4_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1] - L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID - L / 2 - 1];
			V1 = S1 / (L*L);
			V2 = S2 / (L*L) - (V1*V1);
			V3 = 4 * (S3 - col_ID*S1) / (L*L*L);
			V4 = 4 * (S4 - row_ID*S1) / (L*L*L);
		}
		else {
			S1 = L1_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			S2 = L2_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			S3 = L3_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			S4 = L4_dev[(row_ID + L / 2 + (L % 2 > 0) - 1)*M + col_ID + L / 2 + (L % 2 > 0) - 1];
			V1 = S1 / (L*L);
			V2 = S2 / (L*L) - (V1*V1);
			V3 = 4 * (S3 - col_ID*S1) / (L*L*L);
			V4 = 4 * (S4 - row_ID*S1) / (L*L*L);
		}

	}
	output_dev[index] = (V1 - tem_inf[0])*(V1 - tem_inf[0]) + (V2 - tem_inf[1])*(V2 - tem_inf[1]) + (V3 - tem_inf[2])*(V3 - tem_inf[2]) + (V4 - tem_inf[3])*(V4 - tem_inf[3]);
}

int main()
{
	//Just an example here - you are free to modify them
	int I_width, I_height, T_width, T_height;
	float *I, *T; float *L1, *L2, *L3, *L4, *output;
	float *L1_dev, *L2_dev, *L3_dev, *L4_dev, *output_dev, *tem_inf_dev;
	float *L1_row, *L2_row, *L3_row, *L4_row;
	float *L1_dev_row, *L2_dev_row, *L3_dev_row, *L4_dev_row;
	float *I_dev;
	float x1, y1, x2, y2;
	float time_kernel1, time_kernel2, time_kernel3;

	char I_path[] = "lena.bmp";
	char T_path[] = "lena_t.bmp";
	char out_path[] = "output.bmp";
	I = ReadBMP(I_path, &I_width, &I_height);
	T = ReadBMP(T_path, &T_width, &T_height);

	int N = I_height, M = I_width, K = T_width;
	int blocksize = 512;
	int blocknumber0 = N / 128 + (N % 128>0);
	int blocknumber1 = M / 128 + (M % 128>0);
	int blocknumber2 = M*N / blocksize + (((M*N) % blocksize)> 0);

	size_t memsize_of_L = M*N * sizeof(float);

	L1_row = (float *)malloc(memsize_of_L);
	L2_row = (float *)malloc(memsize_of_L);
	L3_row = (float *)malloc(memsize_of_L);
	L4_row = (float *)malloc(memsize_of_L);
	L1 = (float *)malloc(memsize_of_L);
	L2 = (float *)malloc(memsize_of_L);
	L3 = (float *)malloc(memsize_of_L);
	L4 = (float *)malloc(memsize_of_L);
	I = (float *)malloc(memsize_of_L);
	T = (float *)malloc(K*K * sizeof(float));

	output = (float *)malloc(memsize_of_L);
	cudaMalloc((void **)&L1_dev_row, memsize_of_L);
	cudaMalloc((void **)&L2_dev_row, memsize_of_L);
	cudaMalloc((void **)&L3_dev_row, memsize_of_L);
	cudaMalloc((void **)&L4_dev_row, memsize_of_L);
	cudaMalloc((void **)&L1_dev, memsize_of_L);
	cudaMalloc((void **)&L2_dev, memsize_of_L);
	cudaMalloc((void **)&L3_dev, memsize_of_L);
	cudaMalloc((void **)&L4_dev, memsize_of_L);
	cudaMalloc((void **)&I_dev, memsize_of_L);
	cudaMalloc((void **)&output_dev, memsize_of_L);
	cudaMalloc((void **)&tem_inf_dev, 4 * sizeof(float));

	I = ReadBMP(I_path, &I_width, &I_height);
	T = ReadBMP(T_path, &T_width, &T_height);
	
	float tem_inf[4] = { 0,0,0,0 };
	float *Tem_data = getTemdata(T, tem_inf, K);

	cudaMemcpy(I_dev, I, memsize_of_L, cudaMemcpyHostToDevice);
	//kernel1 and kernel2
	cudaEvent_t start_kernel1, end_kernel1;
	cudaEventCreate(&start_kernel1);
	cudaEventCreate(&end_kernel1);
	cudaEventRecord(start_kernel1, 0);
	Row_Cumulate_gpu << <blocknumber0, 128 >> > (I_dev, L1_dev_row, L2_dev_row, L3_dev_row, L4_dev_row, M, N);
	cudaEventRecord(end_kernel1, 0);
	cudaEventSynchronize(start_kernel1);
	cudaEventSynchronize(end_kernel1);
	cudaEventElapsedTime(&time_kernel1, start_kernel1, end_kernel1);

	cudaEvent_t start_kernel2, end_kernel2;
	cudaEventCreate(&start_kernel2);
	cudaEventCreate(&end_kernel2);
	cudaEventRecord(start_kernel2, 0);
	Column_Cumulate_gpu << < blocknumber1, 128 >> > (L1_dev_row, L2_dev_row, L3_dev_row, L4_dev_row, L1_dev, L2_dev, L3_dev, L4_dev, M, N);
	cudaEventRecord(end_kernel2, 0);
	cudaEventSynchronize(start_kernel2);
	cudaEventSynchronize(end_kernel2);
	cudaEventElapsedTime(&time_kernel2, start_kernel2, end_kernel2);

	cudaMemcpy(tem_inf_dev, Tem_data, 4 * sizeof(float), cudaMemcpyHostToDevice);
	//kernel3
	kernel_3 << <blocknumber2, blocksize >> > (L1_dev, L2_dev, L3_dev, L4_dev, output_dev, N, M, K, tem_inf_dev);
	cudaEvent_t start_kernel3, end_kernel3;
	cudaEventCreate(&start_kernel3);
	cudaEventCreate(&end_kernel3);
	cudaEventRecord(start_kernel3, 0);
	kernel_3 << <blocknumber2, blocksize >> > (L1_dev, L2_dev, L3_dev, L4_dev, output_dev, N, M, K, tem_inf_dev);
	cudaEventRecord(end_kernel3, 0);
	cudaEventSynchronize(start_kernel3);
	cudaEventSynchronize(end_kernel3);
	cudaEventElapsedTime(&time_kernel3, start_kernel3, end_kernel3);

	cudaMemcpy(output, output_dev, memsize_of_L, cudaMemcpyDeviceToHost);

	int pos = 0;
	float min = 100;
	for (int i = 0; i < (M *N); i++) {
		if (output[i] < min) {
			min = output[i];
			pos = i;
		}
	}

	float row_pos = pos / M;
	float col_pos = pos % M;
	y1 = row_pos - K / 2;
	x1 = col_pos - K / 2;
	y2 = row_pos + K / 2;
	x2 = col_pos + K / 2;

	printf("Success match.\n");
	printf("Average GPU running time (kernel1): %f ms\n", time_kernel1);
	printf("Average GPU running time (kernel2): %f ms\n", time_kernel2);
	printf("Average GPU running time (kernel3): %f ms\n", time_kernel3);
	MarkAndSave(I_path, x1, y1, x2, y2, out_path);
	free(I); free(T);
	free(L1_row); free(L2_row); free(L3_row); free(L4_row);
	free(L1); free(L2); free(L3); free(L4);
	free(output);
	cudaFree(L1_dev_row); cudaFree(L2_dev_row); cudaFree(L3_dev_row); cudaFree(L4_dev_row);
	cudaFree(L1_dev); cudaFree(L2_dev); cudaFree(L3_dev); cudaFree(L4_dev);
	cudaFree(tem_inf_dev); cudaFree(I_dev); cudaFree(output_dev);
	return 0;
}
