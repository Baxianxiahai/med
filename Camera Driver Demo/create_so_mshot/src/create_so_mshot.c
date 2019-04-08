#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "dvp.h"

int test(char *filename)
{
	printf("start...\r\n");
	dvpStatus status;
	dvpUint32 count;
	dvpHandle h;

	double exp;
	float gain;

    //打开摄像头之前得刷新一下相机后再open才可以使用的
    dvpRefresh(&count);
//    if (count > 8)
//        count = 8;
//
//    for (i = 0; i < count; i++)
//    {
//        if(dvpEnum(i, &info[i]) == DVP_STATUS_OK)
//        {
//            printf("Camera FriendlyName : %s, index=%d\r\n", info[i].FriendlyName,i);
//        }
//    }
//
//    /* No device found */
//    if (count == 0)
//        return 0;

    /* Open the first device */
    status = dvpOpen(0, OPEN_NORMAL, &h);
    if (status != DVP_STATUS_OK)
    {
        printf("Open camera error\r\n");
    }

    status = dvpGetExposure(h,&exp);
    if (status != DVP_STATUS_OK)
       {
         printf("get exposure error\r\n");
       }

    status = dvpGetAnalogGain(h,&gain);
    if (status != DVP_STATUS_OK)
       {
         printf("get gain error\r\n");
       }

    printf("exposure=%lf,gain=%f\r\n",exp,gain);

    //设置自动曝光和自动增益效果
    dvpSetAeMode(h,0);
    /* Start stream */
    status = dvpStart(h);
    if (status != DVP_STATUS_OK)
    {
        printf("get frame error\r\n");
    }

    dvpFrame frame;
    void *p;
    status = dvpGetFrame(h, &frame, &p, 1000);
//    这个名称由Python端传入
//    char* imageFileName = ".jpeg";
//    char* batchpart = "batch#";
//    char* filenamepart = "FileName#";
//    char a[500];

    /* Show frame information */
    printf("frame:%lu, timestamp:%lu, %d*%d, %dbytes, format:%d\r\n",
            frame.uFrameID,
            frame.uTimestamp,
            frame.iWidth,
            frame.iHeight,
            frame.uBytes,
            frame.format);

            dvpSavePicture(&frame, p, filename, 100);

     /* Stop stream */
     status = dvpStop(h);
     if (status != DVP_STATUS_OK)
     {
        printf("stop camera error\r\n");

     }
     dvpClose(h);
     return 0;
}