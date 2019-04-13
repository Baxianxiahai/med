/*
 ============================================================================
 Name        : call_mshot_so_c.c
 Author      : LC
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

int i = 0;
int main(void) {

	mshot_init();
	mshot_capture(1,12,2);
	//mshot_capture_image(3, 4);
}
