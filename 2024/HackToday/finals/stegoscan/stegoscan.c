#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define MIN_IMGSIZE 400 // 20x20
#define MAX_IMGSIZE 900 // 30x30

#define TRIGGER_SIZE 15
uint8_t trigger[] = "hanasuru's-fans";

typedef struct {
  char signature[2];
  uint32_t fileSize;
  uint32_t reserved;
  uint32_t dataOffset;
  uint32_t headerSize;
  int32_t width;
  int32_t height;
  uint16_t colorPlanes;
  uint16_t bitsPerPixel;
  uint32_t compression;
  uint32_t imageSize;
  int32_t horizontalResolution;
  int32_t verticalResolution;
  uint32_t numColors;
  uint32_t importantColors;
} BMPFile;

void error(const char *error) {
  printf("ERROR: %s\n", error);
  exit(-1);
}

BMPFile *loadBitmap(FILE *file) {
  BMPFile *bmp = (BMPFile *)malloc(sizeof(BMPFile));
  if(bmp == NULL)
    error("Bitmap struct heap allocation failed.");

	// Read file headers
	fread(&bmp->signature, sizeof(char), 2, file);
	fread(&bmp->fileSize, sizeof(uint32_t), 1, file);
	fread(&bmp->reserved, sizeof(uint32_t), 1, file);
	fread(&bmp->dataOffset, sizeof(uint32_t), 1, file);
	fread(&bmp->headerSize, sizeof(uint32_t), 1, file);
	fread(&bmp->width, sizeof(int32_t), 1, file);
	fread(&bmp->height, sizeof(int32_t), 1, file);
	fread(&bmp->colorPlanes, sizeof(uint16_t), 1, file);
	fread(&bmp->bitsPerPixel, sizeof(uint16_t), 1, file);
	fread(&bmp->compression, sizeof(uint32_t), 1, file);
	fread(&bmp->imageSize, sizeof(uint32_t), 1, file);
	fread(&bmp->horizontalResolution, sizeof(int32_t), 1, file);
	fread(&bmp->verticalResolution, sizeof(int32_t), 1, file);
	fread(&bmp->numColors, sizeof(uint32_t), 1, file);
	fread(&bmp->importantColors, sizeof(uint32_t), 1, file);

  // signature bytes check
  if(bmp->signature[0] != 'B' || bmp->signature[1] != 'M')
    error("Invalid file signature.");

  // min-max size check
  if(bmp->imageSize < MIN_IMGSIZE || bmp->imageSize > MAX_IMGSIZE)
    error("Invalid bitmap size. The acceptaple resolution range is 20x20 to 30x30.");

  // square bitmap check
  if(bmp->width != bmp->height)
    error("Invalid bitmap resolution. Only square bitmaps are processed.");

  return bmp;
}

int sequenceDetected(const uint8_t *arr, uint32_t size) {
  for(int i=0; i<(size-TRIGGER_SIZE + 1); ++i) {
    if(memcmp(arr+i, trigger, TRIGGER_SIZE) == 0)
      return 1;
  }
  return 0;
}


void scan(const uint8_t *bitmap, uint32_t dim) {
  for(int i = 0; i < dim; ++i) {
    printf("[%02d] : ", i + 1);
    if(sequenceDetected(bitmap+(i * dim), dim))
      printf("FAIL\n");
    else
      printf("PASS\n");
  }
}

int main(int argc, char **argv) {
  if(argc < 2)
    error("No file provided as an argument.");

  size_t len = strlen(argv[1]);
  if(len >= 4 && strcmp(argv[1]+len-4, ".bmp"))
    error("Invalid file extension. Only accepting .bmp files.");

  FILE *file = fopen(argv[1], "rb");
  if(file == NULL)
    error("Failed to open file.");

  BMPFile *bmp = loadBitmap(file);

  fseek(file, bmp->dataOffset, SEEK_SET);

  uint8_t pixelBuf[bmp->imageSize];

  int c = 0, i = 0;
  while((c = fgetc(file)) != EOF)
    pixelBuf[i++] = (uint8_t)c;

  scan(pixelBuf, bmp->width);

  fclose(file);
  return 0;
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}
