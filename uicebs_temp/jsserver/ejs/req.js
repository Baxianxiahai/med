
    var fs = require('fs');
    var msg;
    var baseconf;
    var sysconf;
    var languagelist;
    var language;
    var systeminfo;
    var identifyparameter;
    var mqttconfig;
    function database(data){
    var key = data.action;
    switch(key){
        case "ZH_Medicine_Login":
            var usr = data.body.username;
            var ret = msg.ZH_Medicine_Login;
            ret.status="true";
            ret.ret.username= usr;
            ret.ret.userid= "123123123";
            return JSON.stringify(ret);
        case "ZH_Medicine_Panel_info":

            var ret = msg.ZH_Medicine_Panel_info;
            var filename = ["2x3","3x4","4x6","6x8","8x12","16x24"];
            var temp = GetRandomNum(0,5);
            var body = data.body;
            if(body!=""){
                if(-1 !== filename.indexOf(body)) temp = filename.indexOf(body);
            }
            ret.ret=baseconf[filename[temp]];
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_system_info":
            var ret = msg.ZH_Medicine_system_info;
            ret.ret=systeminfo;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_task_info":
            var ret = msg.ZH_Medicine_task_info;
            var panel = buildrandomresult();
            ret.ret.parameter=systeminfo;
            ret.ret.configure=panel;
            ret.ret.running="false";
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_task_run":
            var ret = msg.ZH_Medicine_task_run;
            var body = data.body;
            var status = body.status;
            var panel = body.configure;
            panel.basic.batch = "test"+GetRandomNum(0,999);
            var retstatus="false";
            if(status == "true") retstatus = "true";
            ret.ret.parameter=systeminfo;
            ret.ret.configure=panel;
            ret.ret.running=retstatus;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_task_running":
            var ret = msg.ZH_Medicine_task_running;

            var retstatus="true";
            var body = data.body;
            var panel = body.configure;
            var arrlength = panel.picture.length;

            for(var i=0;i<arrlength;i++){
                if(panel.picture[i].shooting === "false"){
                    panel.picture[i].shooting = "true";
                    if((i-1)>=0){
                        panel.picture[i-1].videoing = "true";
                        panel.picture[i-1].shooting = "done";
                        var shootnumber = GetRandomNum(1,4);
                        var shootarray = [];
                        for(var j=0;j<shootnumber;j++){
                            shootarray.push("./demo/pic/shoot"
                            +(j+1)+".png");
                        }
                        panel.picture[i-1].shoot = shootarray;
                    }
                    if((i-2)>=0){
                        panel.picture[i-2].videoing = "done";
                        panel.picture[i-2].video = "./demo/video/avorion.mp4";
                        panel.picture[i-2].shooting = "done";
                        panel.picture[i-2].analysising = "true";
                    }
                    if((i-3)>=0){
                        panel.picture[i-3].videoing = "done";
                        panel.picture[i-3].shooting = "done";
                        panel.picture[i-3].analysising = "done";
                        panel.picture[i-3].analysis.resultPic=[];
                        for(var j=0;j<panel.picture[i-3].shoot.length;j++){
                            panel.picture[i-3].analysis.resultPic.push(
                                "./demo/pic/result.png"
                            );
                        }

                        panel.picture[i-3].analysis.result=[];
                        for(var j=0;j<5;j++){
                            panel.picture[i-3].analysis.result.push(
                                {
                                    "title":"result"+j,
                                    "value": ""+GetRandomNum(1,40000)
                                }
                            );
                        }
                    }
                    break;
                }
                if(i === (arrlength-1)){
                    if(panel.picture[i].shooting !== "done"){
                        panel.picture[i].shooting = "done";
                        panel.picture[i].videoing = "true";
                        var shootnumber = GetRandomNum(1,4);
                        var shootarray = [];
                        for(var j=0;j<shootnumber;j++){
                            shootarray.push("./demo/pic/shoot"
                                +(j+1)+".png");
                        }
                        panel.picture[i].shoot = shootarray;
                        if((i-1)>=0){
                            panel.picture[i-1].videoing = "done";
                            panel.picture[i-1].video = "./demo/video/avorion.mp4";
                            panel.picture[i-1].analysising = "true";
                        }
                        if((i-2)>=0){
                            panel.picture[i-2].analysising = "done";
                            panel.picture[i-2].analysis.resultPic=[];
                            for(var j=0;j<panel.picture[i-2].shoot.length;j++){
                                panel.picture[i-2].analysis.resultPic.push(
                                    "./demo/pic/result.png"
                                );
                            }

                            panel.picture[i-2].analysis.result=[];
                            for(var j=0;j<5;j++){
                                panel.picture[i-2].analysis.result.push(
                                    {
                                        "title":"result"+j,
                                        "value": ""+GetRandomNum(1,40000)
                                    }
                                );
                            }
                        }
                    }else if(panel.picture[i].videoing !== "done"){
                        panel.picture[i].videoing = "done";
                        panel.picture[i].video = "./demo/video/avorion.mp4";
                        panel.picture[i].analysising = "true";
                        if((i-1)>=0){
                            panel.picture[i-1].analysising = "done";
                            panel.picture[i-1].analysis.resultPic=[];
                            for(var j=0;j<panel.picture[i-1].shoot.length;j++){
                                panel.picture[i-1].analysis.resultPic.push(
                                    "./demo/pic/result.png"
                                );
                            }
                            panel.picture[i-1].analysis.result=[];
                            for(var j=0;j<5;j++){
                                panel.picture[i-1].analysis.result.push(
                                    {
                                        "title":"result"+j,
                                        "value": ""+GetRandomNum(1,40000)
                                    }
                                );
                            }
                        }
                    }else{
                        panel.picture[i].analysising = "done";
                        panel.picture[i].analysis.resultPic=[];
                        for(var j=0;j<panel.picture[i].shoot.length;j++){
                            panel.picture[i].analysis.resultPic.push(
                                "./demo/pic/result.png"
                            );
                        }
                        panel.picture[i].analysis.result=[];
                        for(var j=0;j<5;j++){
                            panel.picture[i].analysis.result.push(
                                {
                                    "title":"result"+j,
                                    "value": ""+GetRandomNum(1,40000)
                                }
                            );
                        }
                        retstatus = "false"
                    }
                }
            }
            ret.ret.parameter=systeminfo;
            ret.ret.configure=panel;
            ret.ret.running=retstatus;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_set_temp_conf":
            var ret = msg.ZH_Medicine_set_temp_conf;
            identifyparameter=jsondeepcopy(data.body);
            ret.ret=identifyparameter;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_get_temp_conf":
            var ret = msg.ZH_Medicine_get_temp_conf;
            ret.ret=identifyparameter;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_run_temp_analysis":
            var ret = msg.ZH_Medicine_set_temp_conf;
            identifyparameter=jsondeepcopy(data.body);
            ret.ret=identifyparameter;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_get_temp_task_status":
            var body = jsondeepcopy(data.body);
            body.analysis.result = [];
            body.analysis.result.push(
                {
                    "title":"temptrain",
                    "value":"true"
                }
            );
            var tempret;
            if(15>= GetRandomNum(1,20)){
                tempret = {
                    "status":"false"
                }
            }else{
                tempret = {
                    "status":"true",
                    "result": body
                }
            }
            var ret = msg.ZH_Medicine_set_temp_conf;
            ret.ret=tempret;
            ret.status="true";
            ret.msg="process"+GetRandomNum(0,100)+"%";
            return JSON.stringify(ret);
        case "ZH_Medicine_save_temp_conf":
            var ret = msg.ZH_Medicine_save_temp_conf;
            identifyparameter=jsondeepcopy(data.body);
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_sys_config":
            var ret = msg.ZH_Medicine_sys_config;
            ret.ret=sysconf;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_sys_config_save":
            var ret = msg.ZH_Medicine_sys_config_save;
            sysconf=jsondeepcopy(data.body);
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_sys_language":
            var ret = msg.ZH_Medicine_sys_language;
            var defaultlanguage = data.body.default;
            if(languagelist.default !== defaultlanguage){
                reloadlanguage(defaultlanguage);
            }
            ret.ret=language;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_sys_language_list":
            var ret = msg.ZH_Medicine_sys_language_list;
            ret.ret=languagelist;
            ret.status="true";
            return JSON.stringify(ret);
        case "ZH_Medicine_mqtt_conf":
            var ret = msg.ZH_Medicine_mqtt_conf;
            ret.ret=mqttconfig;
            ret.status="true";
            return JSON.stringify(ret);
        default:
            console.log("Don't understand query key:"+key);
            return JSON.stringify(msg.ZH_Medicine_default);
    }
}
    function mqttdatabase(data){}
    function check_usr(data){
    }
    function req_test(){
    }
    function GetRandomNum(Min,Max)
    {
        var Range = Max - Min;
        var Rand = Math.random();
        return(Min + Math.round(Rand * Range));
    }

    function prepareconf(){
        console.log("Start to prepare the configuration structure.");

        msg = JSON.parse(jsReadFiles("./msg/message.json"));
        baseconf={};
        var templist = getfilelist("./baseconf/plateconf/");
        for(var i=0;i<templist.length;i++){
            baseconf[templist[i].split(".")[0]]=JSON.parse(jsReadFiles("./baseconf/plateconf/"+templist[i]));
        }
        sysconf = JSON.parse(jsReadFiles("./sysconf/configure.json"));
        languagelist = JSON.parse(jsReadFiles("./sysconf/supportlanguage.json"));

        language=JSON.parse(jsReadFiles("./language/language_"+languagelist.default+".json"));
        systeminfo= JSON.parse(jsReadFiles("./sysconf/systeminfo.json"));
        identifyparameter= JSON.parse(jsReadFiles("./sysconf/IdentifyParameter.json"));
        mqttconfig = JSON.parse(jsReadFiles("./sysconf/mqtt.json"));
        console.log("config load finish");
        //console.log("baseconf:");
        //console.log(JSON.stringify(baseconf));
    }


    function getfilelist(filePath){
        var list = fs.readdirSync(filePath);
        return list;
    }

    function jsReadFiles(files) {
        var output = fs.readFileSync(files, 'utf8');
        return output;
    }
    function jsWriteFiles(files,data) {
        fs.writeFileSync(files, data);
    }
    function jsondeepcopy(data){
        return JSON.parse(JSON.stringify(data));
    }
    function buildoneresult(series){
        var subpic={
            "series":series,
            "shoot":[],
            "video":"./demo/video/avorion.mp4",
            "shooting":"done",
            "videoing":"done",
            "analysising":"done",
            "analysis":{}
        }
        var shootnumber= GetRandomNum(1,4);
        var resultpic=[]
        for(var i=0;i<shootnumber;i++){
            subpic.shoot.push("./demo/pic/shoot"+(i+1)+".png");
            resultpic.push("./demo/pic/result.png");
        }
        var resultAna = [];
        for(var i=0;i<5;i++){
            resultAna.push({
                "title":"result"+i,
                "value":""+GetRandomNum(1,1000000)
            });
        }
        subpic.analysis={
            'resultPic':resultpic,
            'result':resultAna
        };
        return subpic;
    }
    function buildrandomresult(){
        var filename = ["2x3","3x4","4x6","6x8","8x12","16x24"];
        var temp = GetRandomNum(0,5);
        var retarray=jsondeepcopy(baseconf[filename[temp]]);
        retarray.basic.batch="12312312312";
        if(temp === 0 ){
            for(var i=0;i<retarray.basic.longitude.length;i++){
                if(10>GetRandomNum(0,100)){
                    continue;
                }else{
                    retarray.picture.push(buildoneresult(retarray.basic.longitude[i]));
                }

            }
        }else{
            for(var i=0;i<retarray.basic.latitude.length;i++){
                for(var j=0;j<retarray.basic.longitude.length;j++){
                    if(30>GetRandomNum(0,100)){
                        continue;
                    }else{
                        retarray.picture.push(buildoneresult(
                            retarray.basic.latitude[i]+
                            retarray.basic.longitude[j]));
                    }
                }
            }
        }

        return retarray;


    }
    function reloadlanguage(defaultlang){
        language=JSON.parse(jsReadFiles("./language/language_"+defaultlang+".json"));
        languagelist.default = defaultlang;
        jsWriteFiles("./sysconf/supportlanguage.json",JSON.stringify(languagelist));

    }

    exports.req_test=req_test;
    exports.database=database;
    exports.check_usr=check_usr;
    exports.prepareconf=prepareconf;
    exports.mqttdatabase=mqttdatabase;
    exports.GetRandomNum=GetRandomNum;