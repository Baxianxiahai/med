/*
 ============================================================================
 Name        : ping.c
 Author      : LC:maybe this can not work
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <netdb.h>
#include <sys/socket.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    char   *ptr, **pptr;
    struct hostent *hptr;
    char   str[500];
    ptr = argv[1];

    if((hptr = gethostbyname("www.baidu.com")) == NULL)
    {
        printf(" gethostbyname error for host:%s\n", ptr);
        return 0;
    }
    printf("official hostname:%s\n",hptr->h_name);

    for(pptr = hptr->h_aliases; *pptr != NULL; pptr++)
    	printf("alias:%s\n",*pptr);
    printf("type=%d\n",hptr->h_addrtype);
    printf("type\n");
    switch(hptr->h_addrtype)
    {
        case AF_INET:
        	printf("in this\n");
        	pptr=hptr->h_addr_list;

        	for(; *pptr!=NULL; pptr++)
        	    printf("address:%s\n",inet_ntop(hptr->h_addrtype, *pptr, str, sizeof(str)));
        	printf("first address:%s\n",inet_ntop(hptr->h_addrtype, hptr->h_addr[0], str, sizeof(str)));
        	break;
        case AF_INET6:
        default:
            printf("unknown address type\n");
        break;
    }
    return 0;
}
