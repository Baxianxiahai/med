#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "dvp.h"


//LC:以下建立分布的摄像头操作，目的是实现相机初始化消息有返回，实际上初始化后就关闭了摄像头，后续切换到校准界面，或者正式开始拍摄时还需再次open的
int mshot_init(void)
{
	printf("Init camera...\r\n");
	dvpUint32 count;
	dvpStatus status;
	dvpRefresh(&count);
	dvpHandle h;
	status = dvpOpen(0, OPEN_NORMAL, &h);
	if (status != DVP_STATUS_OK)
    {
	   printf("Open camera error\r\n");
	   return -1;
	}
	else
	{
		printf("Open camera successfully\r\n");
		dvpStop(h);
		dvpClose(h);
		return 0;
	}

}
/*
#define  96_board    5
#define  48_board    4
#define  24_board    3
#define  12_board    2
#define  6_board     1

*/
int mshot_capture(int i ,int j, int boardtype)
{
	dvpStatus status;
	dvpHandle h;
	dvpUint32 count;
	double exp;
    float gain;

	dvpRefresh(&count);
 /* Open the first device */
	status = dvpOpen(0, OPEN_NORMAL, &h);
	/* Start stream */
	status = dvpStart(h);
	if (status != DVP_STATUS_OK)
	{
		printf("get frame error\r\n");
	}

	//拼接文件名称
	char* imageFileType = ".jpg";
	char  batchpart[500] = "batch#";
	char* filenamepart = "FileName#";
	char a[10];
	char* b;
    char *globalname[97];
    if (5 == boardtype ){
    printf("this is the 96_board\r\n");
	char *name[97] = {
						"A0", "A1", "A2","A3","A4","A5","A6","A7","A8","A9","A10", "A11","A12",\
						"B1", "B2", "B3","B4","B5","B6","B7","B8","B9","B10","B11","B12",\
						"C1", "C2", "C3","C4","C5","C6","C7","C8","C9","C10","C11","C12",\
						"D1", "D2", "D3","D4","D5","D6","D7","D8","D9","D10","D11","D12",\
						"E1", "E2", "E3","E4","E5","E6","E7","E8","E9","E10","E11","E12",\
						"F1", "F2", "F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",\
						"G1", "G2", "G3","G4","G5","G6","G7","G8","G9","G10","G11","G12",\
						"H1", "H2", "H3","H4","H5","H6","H7","H8","H9","H10","H11","H12"};
    memcpy(globalname,name,sizeof(name));

    }
    if (4 == boardtype){
    printf("this is the 48_board\r\n");
	char *name[49] = {
						"A0", "A1", "A2","A3","A4","A5","A6","A7","A8",\
							"B1", "B2", "B3","B4","B5","B6","B7","B8",\
							"C1", "C2", "C3","C4","C5","C6","C7","C8",\
							"D1", "D2", "D3","D4","D5","D6","D7","D8",\
							"E1", "E2", "E3","E4","E5","E6","E7","E8",\
							"F1", "F2", "F3","F4","F5","F6","F7","F8"};
	memcpy(globalname,name,sizeof(name));
    }
    if (3 == boardtype){
    printf("this is the 24_board\r\n");
	char *name[25] = {
						"A0", "A1", "A2","A3","A4","A5","A6",\
							"B1", "B2", "B3","B4","B5","B6",\
							"C1", "C2", "C3","C4","C5","C6",\
							"D1", "D2", "D3","D4","D5","D6"};
	memcpy(globalname,name,sizeof(name));
    }
    if (2 == boardtype){
    printf("this is the 12_board\r\n");
	char *name[13] = {
						"A0", "A1", "A2","A3","A4",\
							"B1", "B2", "B3","B4",\
							"C1", "C2", "C3","C4"};
	memcpy(globalname,name,sizeof(name));
	}
    if (1 == boardtype){
    printf("this is the 6_board\r\n");
	char *name[7] = {
						"A0", "A1", "A2","A3",\
							"B1", "B2", "B3"};
	memcpy(globalname,name,sizeof(name));
  	}


	char * combinename(int i, int j)
	{
		 char* totalname;
		 sprintf(a,"%d",i);
		 totalname = strcat(batchpart,a);
		 totalname = strcat(totalname,filenamepart);
		 b= globalname[j];
		 totalname = strcat(totalname,b);
		 totalname = strcat(totalname,imageFileType);
		 return totalname;
	}


	char* imageFileName;

	imageFileName = combinename(i,j);

	dvpFrame frame;
	void *p;
	status = dvpGetFrame(h, &frame, &p, 1000);

	/* Show frame information */
	printf("frame:%lu, timestamp:%lu, %d*%d, %dbytes, format:%d\r\n",
			frame.uFrameID,
			frame.uTimestamp,
			frame.iWidth,
			frame.iHeight,
			frame.uBytes,
			frame.format);

	 status = dvpSavePicture(&frame, p, imageFileName, 100);
	 if (status == DVP_STATUS_OK)
	 {
		 printf("capture picture once successfully\r\n");
	 }
	 /* Stop stream */
	 status = dvpStop(h);
	 if (status != DVP_STATUS_OK)
	 {
		printf("stop camera error\r\n");
	 }

	 dvpClose(h);
	 return 0;

}

//LC:下面的获取图片是直接初始化摄像头，然后获取图片的整体操作
int mshot_capture_image(int i, int j)
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


    //拼接文件名称
    char* imageFileType = ".jpg";
    char  batchpart[500] = "batch#";
    char* filenamepart = "FileName#";
    char a[10];
    char* b;

    char *name[97] = {
        		        "A0", "A1", "A2","A3","A4","A5","A6","A7","A8","A9","A10", "A11","A12",\
        		        "B1", "B2", "B3","B4","B5","B6","B7","B8","B9","B10","B11","B12",\
        		        "C1", "C2", "C3","C4","C5","C6","C7","C8","C9","C10","C11","C12",\
        		        "D1", "D2", "D3","D4","D5","D6","D7","D8","D9","D10","D11","D12",\
        		        "E1", "E2", "E3","E4","E5","E6","E7","E8","E9","E10","E11","E12",\
        		        "F1", "F2", "F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",\
        		        "G1", "G2", "G3","G4","G5","G6","G7","G8","G9","G10","G11","G12",\
        		        "H1", "H2", "H3","H4","H5","H6","H7","H8","H9","H10","H11","H12"};



    char * combinename(int i, int j)
    {
         char* totalname;
         sprintf(a,"%d",i);
         totalname = strcat(batchpart,a);
         totalname = strcat(totalname,filenamepart);
         b= name[j];
         totalname = strcat(totalname,b);
         totalname = strcat(totalname,imageFileType);
         return totalname;
    }


    char* imageFileName;

    imageFileName = combinename(i,j);

    dvpFrame frame;
    void *p;
    status = dvpGetFrame(h, &frame, &p, 1000);

    /* Show frame information */
    printf("frame:%lu, timestamp:%lu, %d*%d, %dbytes, format:%d\r\n",
            frame.uFrameID,
            frame.uTimestamp,
            frame.iWidth,
            frame.iHeight,
            frame.uBytes,
            frame.format);

     status = dvpSavePicture(&frame, p, imageFileName, 100);
     if (status == DVP_STATUS_OK)
     {
         printf("capture picture once successfully\r\n");
     }
     /* Stop stream */
     status = dvpStop(h);
     if (status != DVP_STATUS_OK)
     {
        printf("stop camera error\r\n");
     }
     dvpClose(h);
     return 0;
}



