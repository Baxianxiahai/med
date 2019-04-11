/*
 ============================================================================
 Name        : call_so_c.c
 Author      : LC
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "call_so_c.h"

int ret = 0;
int main(void) {
    ret = test_add(2,3);
    printf("ret=%d\r\n",ret);
    test();

}
