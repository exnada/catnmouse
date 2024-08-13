// gcc -shared -o libdrawmaze.so -fPIC drawmaze.c

void connect();
int randNum();
int addNum(int a, int b);
int showMaze(int width, int height, int *maze);
int drawMaze(int width, int height, int *maze);
// void read_png(char *file_name);
// void read_png(char *file_name);

typedef struct {
  uint8_t red;
  uint8_t green;
  uint8_t blue;
  uint8_t alpha;
} pixel_t;

/* A picture. */

typedef struct {
  size_t width;
  size_t height;
  pixel_t *pixels;
} bitmap_t;

static int save_png_to_file(bitmap_t *bitmap, const char *path);
