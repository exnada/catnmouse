// gcc -shared -o libdrawmaze.so -fPIC drawmaze.c
#include <png.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "drawmaze.h"
 
void connect()
{
    printf("Connected to C extension...\n");
}
 
//return random value in range of 0-50
int randNum()
{
    int nRand = rand() % 50; 
    return nRand;
}
 
//add two number and return value
int addNum(int a, int b)
{
    int nAdd = a + b;
    return nAdd;
}


// print maze array as values
int showMaze(int width, int height, int *maze)
{
	printf("[\n");
	for (int h=0; h<height; h++) {
		printf(" [ ");
		for (int w=0; w<width; w++){
			printf("%i ", maze[width*h+w]);
		}
		printf("]\n");
	}
	printf("]\n");
}


int drawMaze(int width, int height, int *maze) {	
	printf("drawMaze(): starting...\n");
	// const int wall_thickness = 3;
	// const int cell_thickness = 22;
	// const int wall_thickness = 4;
	// const int cell_thickness = 36;
	// const int wall_thickness = 20;
	// const int cell_thickness = 20;
	const int wall_thickness = 2;
	const int cell_thickness = 18;

	bitmap_t img_maze;
	int imgwidth = (width+1)*wall_thickness + width*cell_thickness;
	int imgheight = (height+1)*wall_thickness + height*cell_thickness;
	img_maze.width = imgwidth;
	img_maze.height = imgheight;
	img_maze.pixels = calloc(img_maze.width * img_maze.height, sizeof(pixel_t));

	if (!img_maze.pixels){
		fprintf(stderr, "ABORT: cannot allocate pixel array for png output.\n");
		return -1;
	}

	int status = 0;
	char* filename = "pics/testimg.png";

	pixel_t *pixel = img_maze.pixels;
	int maze_val = -1;
	for (int wv=0; wv<wall_thickness; wv++){ //vertical wall thickness
		for (int wh=0; wh<wall_thickness; wh++) { // horizontal wall
			maze_val = maze[0];
			pixel->red = 255*(1-maze_val);
			pixel->green = 255*(1-maze_val);
			pixel->blue = 255*(1-maze_val);
			pixel->alpha = 255;
			pixel++;
			// printf("%d ", maze_val);
		}
		// printf(" |x| ");
		for (int x=0; x<width; x++){
			for (int ch=0; ch<cell_thickness; ch++) { // horizontal cell
				maze_val = maze[2*x+1];
				pixel->red = 255*(1-maze_val);
				pixel->green = 255*(1-maze_val);
				pixel->blue = 255*(1-maze_val);
				pixel->alpha = 255;
				pixel++;
				// printf("%d ", maze_val);
			}
			// printf(" | ");
			for (int wh=0; wh<wall_thickness; wh++) { // horizontal wall
				maze_val=maze[2*(x+1)];
				pixel->red = 255*(1-maze_val);
				pixel->green = 255*(1-maze_val);
				pixel->blue = 255*(1-maze_val);
				pixel->alpha = 255;
				pixel++;
				// printf("%d ", maze_val);
			}
			// printf(" || ");
			// pixel->red = (int) (255 * (maze[w]))
		}
		// printf("\n");
	}

	for (int y=0; y<height; y++){
		for (int cv=0; cv<cell_thickness; cv++){ //vertical cell thickness
			maze_val = maze[(2*y+1)*(2*width+1) + 0];
			for (int wh=0; wh<wall_thickness; wh++) { // horizontal wall
				pixel->red = 255*(1-maze_val);
				pixel->green = 255*(1-maze_val);
				pixel->blue = 255*(1-maze_val);
				pixel->alpha = 255;
				pixel++;
				// printf("%d ", maze_val);
			}
			// printf(" |x| ");
			for (int x=0; x<width; x++){
				// maze_val = maze[(2*y+1)*width + 2*x+1];
				maze_val = maze[(2*y+1)*(2*width+1) + 2*x+1];
				for (int ch=0; ch<cell_thickness; ch++) { // horizontal cell
					pixel->red = 255*(1-maze_val);
					pixel->green = 255*(1-maze_val);
					pixel->blue = 255*(1-maze_val);
					pixel->alpha = 255;
					pixel++;
					// printf("%d ", maze_val);
				}
				// printf(" | ");
				maze_val = maze[(2*y+1)*(2*width+1) + 2*(x+1)];
				for (int wh=0; wh<wall_thickness; wh++) { // horizontal wall
					pixel->red = 255*(1-maze_val);
					pixel->green = 255*(1-maze_val);
					pixel->blue = 255*(1-maze_val);
					pixel->alpha = 255;
					pixel++;
					// printf("%d ", maze_val);
				}
				// printf(" || ");
				// pixel->red = (int) (255 * (maze[w]))
			}
			// printf("\n");
		}
		for (int wv=0; wv<wall_thickness; wv++){ //vertical wall thickness
			maze_val = maze[(2*(y+1))*(2*width+1) + 0];
			for (int wh=0; wh<wall_thickness; wh++) { // horizontal wall
				pixel->red = 255*(1-maze_val);
				pixel->green = 255*(1-maze_val);
				pixel->blue = 255*(1-maze_val);
				pixel->alpha = 255;
				pixel++;
				// printf("%d ", maze_val);
			}
			// printf(" |x| ");
			for (int x=0; x<width; x++){
				maze_val = maze[(2*(y+1))*(2*width+1) + 2*x+1];
				for (int ch=0; ch<cell_thickness; ch++) { // horizontal cell
					pixel->red = 255*(1-maze_val);
					pixel->green = 255*(1-maze_val);
					pixel->blue = 255*(1-maze_val);
					pixel->alpha = 255;
					pixel++;
					// printf("%d ", maze_val);
				}
				// printf(" | ");
				maze_val = maze[(2*(y+1))*(2*width+1) + 2*(x+1)];
				for (int wh=0; wh<wall_thickness; wh++) { // horizontal wall
					pixel->red = 255*(1-maze_val);
					pixel->green = 255*(1-maze_val);
					pixel->blue = 255*(1-maze_val);
					pixel->alpha = 255;
					pixel++;
					// printf("%d ", maze_val);
				}
				// printf(" || ");
				// pixel->red = (int) (255 * (maze[w]))
			}
			// printf("\n");
		}

	}

	if (save_png_to_file(&img_maze, filename)){
		fprintf(stderr, "ABORT: error writing png file %s.\n", filename);
		status = -1;
	}

	free(img_maze.pixels);
	printf("drawMaze(): done.\n");
	return status;
}


static int save_png_to_file(bitmap_t *bitmap, const char *path) {
  FILE *fp;
  png_structp png_ptr = NULL;
  png_infop info_ptr = NULL;
  size_t x, y;
  png_byte **row_pointers = NULL;
  /* "status" contains the return value of this function. At first
     it is set to a value which means 'failure'. When the routine
     has finished its work, it is set to a value which means
     'success'. */
  int status = -1;
  /* The following number is set by trial and error only. I cannot
     see where it it is documented in the libpng manual.
  */
  // int pixel_size = 3;
  int pixel_size = 4;
  int depth = 8;

  fp = fopen(path, "wb");
  if (!fp) {
  	fprintf(stderr, "ABORT: unable to open file %s\n", path);
    return status;
  }

  png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
  if (png_ptr == NULL) {
    // goto png_create_write_struct_failed;
    fclose(fp);
    return status;
  }

  info_ptr = png_create_info_struct(png_ptr);
  if (info_ptr == NULL) {
    // goto png_create_info_struct_failed;
    png_destroy_write_struct(&png_ptr, &info_ptr);
    fclose(fp);
    return status;
  }

  /* Set up error handling. */
  if (setjmp(png_jmpbuf(png_ptr))) {
    // goto png_failure;
    png_destroy_write_struct(&png_ptr, &info_ptr);
    fclose(fp);
    return status;
  }

  /* Set image attributes. */

  png_set_IHDR(png_ptr, info_ptr, bitmap->width, bitmap->height, depth,
               PNG_COLOR_TYPE_RGBA, PNG_INTERLACE_NONE,
               PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT);

  /* Initialize rows of PNG. */

  row_pointers = png_malloc(png_ptr, bitmap->height * sizeof(png_byte *));
  for (y = 0; y < bitmap->height; y++) {
    png_byte *row =
        png_malloc(png_ptr, sizeof(uint8_t) * bitmap->width * pixel_size);
    row_pointers[y] = row;
    for (x = 0; x < bitmap->width; x++) {
      pixel_t *pixel = bitmap->pixels + bitmap->width * y + x;
      *row++ = pixel->red;
      *row++ = pixel->green;
      *row++ = pixel->blue;
      *row++ = pixel->alpha;
    }
  }

  /* Write the image data to "fp". */

  png_init_io(png_ptr, fp);
  png_set_rows(png_ptr, info_ptr, row_pointers);
  png_write_png(png_ptr, info_ptr, PNG_TRANSFORM_IDENTITY, NULL);

  /* The routine has successfully written the file, so we set
     "status" to a value which indicates success. */

  status = 0;

  for (y = 0; y < bitmap->height; y++) {
    png_free(png_ptr, row_pointers[y]);
  }
  png_free(png_ptr, row_pointers);

  png_destroy_write_struct(&png_ptr, &info_ptr);
  fclose(fp);
  return status;
}
