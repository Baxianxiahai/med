#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "dvp.h"


int mshot_init(void);
int mshot_capture(int i ,int j, int boardtype);
int mshot_capture_image(int i, int j ,int boardtype);


char * combinename(int i, int j);

