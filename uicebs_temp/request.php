<?php
header("Content-type:text/html;charset=utf-8");
function _encode($arr)
{
  $na = array();
  foreach ( $arr as $k => $value ) {
    $na[_urlencode($k)] = _urlencode ($value);
  }
  return addcslashes(urldecode(json_encode($na)),"\r\n");
}

function _urlencode($elem)
{
  if(is_array($elem)&&(!(empty($elem)))){
    foreach($elem as $k=>$v){
      $na[_urlencode($k)] = _urlencode($v);
    }
    return $na;
  }
  if(is_array($elem)&&empty($elem)){
	  return $elem;
  }
  return urlencode($elem);
}
function filenew($name,$content){
    $newfile=fopen("./json/".$name.".json","w");
    fwrite($newfile,$content);
    fclose($newfile);
}
function filemod($name,$content){
    $modfile=fopen("./json/".$name.".json","w+") ;
    fwrite($modfile,$content);
    fclose($modfile);
}
function tempmod($content){
    $modfile=fopen("./sysconf/IdentifyParameter.json","w+") ;
    fwrite($modfile,$content);
    fclose($modfile);
}
function confmod($content){
    $modfile=fopen("./sysconf/configure.json","w+") ;
    fwrite($modfile,$content);
    fclose($modfile);
}
function languagemod($content){
    $modfile=fopen("./sysconf/supportlanguage.json","w+") ;
    fwrite($modfile,$content);
    fclose($modfile);
}
function getfiles($path,$type){
    $ret = array();
    if(!file_exists($path)) return $ret;
    foreach(glob($path."/*".$type) as $afile){
        if(is_dir($afile))
        {
            //getfiles($afile.'/*.'.$type);
        } else {
            //echo $afile.'<br />';
            $json_string = file_get_contents($afile);
            //echo print_r($json_string,true);            //��ӡ�ļ�������
            //echo "<br>";

            $obj=json_decode($json_string,true);
            //print_r($obj);
            //echo '<br>'.$obj['name'];
            //echo '<br>'.$obj['icon'];
            //echo '<br>'.$obj['owner'];
            //echo '<br>'.$obj['description'];

            $map= array(
                'index'=>'123',
                'name'=>$obj['name'],
                'icon'=>$obj['icon'],
                'owner'=>$obj['owner'],
                'description'=>$obj['description']
            );
            array_push($ret,$map);
        }
    }
    return $ret;
}
function geticonlist(){
    $path="./svg/";
    $type=".svg";
    $ret = array();
    if(!file_exists($path)) return $ret;
    foreach(glob($path."/*".$type) as $afile){
        if(is_dir($afile))
        {
            //getfiles($afile.'/*.'.$type);
        } else {
            array_push($ret,basename($afile));
        }
    }
    return $ret;
}
function getfiledetail($path){
    $ret = "";
    if(!file_exists($path)) {
        //echo $path." is not exist!";
        return "";
    }
    $afile=$path;
    $json_string = file_get_contents($afile);
    return $json_string;
}
function deletefile($path){
    $ret = "";
    if(!file_exists($path)) {
        //echo $path." is not exist!";
        return false;
    }
    $afile=$path;
    $result = unlink ($path);
    return $result;
}
function get_file_list($dir,$type){
    $ret = array();
    if(!file_exists($ff)) $ret;
    $handle = opendir($ff);
    $i=0;
    while(false !== $file=(readdir($handle))){
        if($file !== "." && $file!=".."){
            $i++;
        }
    }
    return $i;
}
/**
        字符串GBK转码为UTF-8，数字转换为数字。
    */
    function ct2($s){
        if(is_numeric($s)) {
            return intval($s);
        } else {
            return iconv("GBK","UTF-8",$s);
        }
    }
    /**
        批量处理gbk->utf-8
    */
    function icon_to_utf8($s) {
      if(is_array($s)) {
        foreach($s as $key => $val) {
          $s[$key] = icon_to_utf8($val);
        }
      } else {
          $s = ct2($s);
      }
      return $s;
    }
    /**************************************************************
    *
    *    使用特定function对数组中所有元素做处理
    *    @param    string    &$array        要处理的字符串
    *    @param    string    $function    要执行的函数
    *    @return boolean    $apply_to_keys_also        是否也应用到key上
    *    @access public
    *
    *************************************************************/
    function arrayRecursive(&$array, $function, $apply_to_keys_also = false)
    {
        foreach ($array as $key => $value) {
            if (is_array($value)) {
                arrayRecursive($array[$key], $function, $apply_to_keys_also);
            } else {
                $array[$key] = $function($value);
            }
            if ($apply_to_keys_also && is_string($key)) {
                $new_key = $function($key);
                if ($new_key != $key) {
                    $array[$new_key] = $array[$key];
                    unset($array[$key]);
                }
            }
        }
    }
    /**************************************************************
    *
    *    将数组转换为JSON字符串（兼容中文）
    *    @param    array    $array        要转换的数组
    *    @return string        转换得到的json字符串
    *    @access public
    *
    *************************************************************/
    function JSON($array) {
        arrayRecursive($array, 'urlencode', true);
        $json = json_encode($array);
        return urldecode($json);
    }


    function buildoneresult($seriesNo){
        $series = $seriesNo;
        $videoing="done";
        $shooting="done";
        $analysising="done";
        $video="./demo/video/avorion.mp4";
        $shootnumber = rand(1,4);
        $shootarray = array();
        for($k=0;$k<$shootnumber;$k++){
            array_push($shootarray,"./demo/pic/shoot".(string)($k+1).".png");
        }
        $resultPic=array();
        for($k=0;$k<$shootnumber;$k++){
            array_push($resultPic,"./demo/pic/result.png");
        }
        $resultAna=array();
         for($k=0;$k<5;$k++){
            $resultitem=array(
                'title'=>'result'.(string)$k,
                'value'=>(string)rand(0,1000)
            );
            array_push($resultAna,$resultitem);
         }
         $result=array(
             'resultPic'=>$resultPic,
             'result'=>$resultAna
         );
         $subpic=array(
              "series"=>$series,
              "shoot"=>$shootarray,
              "video"=>$video,
              "shooting"=>$shooting,
              "videoing"=>$videoing,
              "analysising"=>$analysising,
              "analysis"=>$result
          );
          return $subpic;
    }
    function buildrandomresult(){

        $filename = array("2x3","3x4","4x6","6x8","8x12","16x24");
        $x = rand(0,5);
        $retarray = json_decode(getfiledetail("./baseconf/plateconf/".$filename[$x].".json"),true);
        $retarray['basic']['batch']="1231231231";
        if($x==0){
            for($i=0;$i<count($retarray["basic"]["longitude"]);$i++){
                    $y = rand(0,100);
                    if($y<10) continue;
                    else{
                        $series = $retarray["basic"]["longitude"][$i];
                        array_push($retarray["picture"],buildoneresult($series));
                    }
            }
        }else{
            for($i=0;$i<count($retarray["basic"]["latitude"]);$i++){
                    for($j=0;$j<count($retarray["basic"]["longitude"]);$j++){
                        $y = rand(0,100);
                        if($y<30) continue;
                        else{
                            $series = $retarray["basic"]["latitude"][$i].$retarray["basic"]["longitude"][$j];
                            array_push($retarray["picture"],buildoneresult($series));
                        }
                    }
                }
        }
        return $retarray;



    }
$request_body = file_get_contents('php://input');
//echo $request_body;
$payload = json_decode($request_body,true);
//echo $payload;
$key=$payload["action"];
//echo $key;
switch ($key){
    case "ZH_Medicine_Login": //Use Wechat to login the Server, response is the userID in system.
    /*
         var body = {
                        username:username,
                        password:password};
         var map={
         action:"HCU_Wechat_Bonding",
         type:"query",
         body: body,
         user:"null"
         };
        * */
            $body=$payload["body"];

            $user=array(
                'username'=> $body["username"],
                'userid'=>'123123123'
            );
            $sta='true';
            $retval=array(
                'status'=>$sta,
                'auth'=>'true',
                'ret'=>$user,
                'msg'=>'12345'
            );

            $jsonencode = _encode($retval);
            echo $jsonencode; break;
    case "ZH_Medicine_Panel_info":
            $filename = array("2x3","3x4","4x6","6x8","8x12","16x24");
            $body=$payload["body"];
            $x= -1;
            if($body!=""){
                $x=$filename.indexOf($body,0);
            }
            if($x<0) $x = rand(0,5);
            $retarray = getfiledetail("./baseconf/plateconf/".$filename[$x].".json");
            //echo("./baseconf/plateconf/".$filename[$x].".json");
            //echo($retarray);
            $obj=json_decode($retarray,true);
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'ret'=>$obj,
                'msg'=>''
            );
            $jsonencode = _encode($retval);
            echo $jsonencode; break;
    case "ZH_Medicine_system_info":
                $retarray;
                $retarray = getfiledetail("./sysconf/systeminfo.json");

                 $obj=json_decode($retarray,true);
                $retval=array(
                    'status'=>'true',
                    'auth'=>'true',
                    'ret'=>$obj,
                    'msg'=>''
                );

                $jsonencode = _encode($retval);
                echo $jsonencode; break;
    case "ZH_Medicine_task_info":
            $body=$payload["body"];
            //$panel = $body["configure"];
            $panel = buildrandomresult();
                $retarray;
                $retarray = getfiledetail("./sysconf/systeminfo.json");

                 $obj=json_decode($retarray,true);
                 $temp = array(
                    'parameter'=>$obj,
                    'configure'=>$panel,
                    'running'=> 'false'
                 );
                $retval=array(
                    'status'=>'true',
                    'auth'=>'true',
                    'ret'=>$temp,
                    'msg'=>''
                );

                $jsonencode = _encode($retval);
                echo $jsonencode; break;
    case "ZH_Medicine_task_run":
        $body=$payload["body"];
        $status = $body["status"];
        $panel = $body["configure"];
        $panel["basic"]["batch"]="test".(string)rand(0,999);
        $retstatus="false";
        if($status == "true") $retstatus="true";
                    $retarray;
                    $retarray = getfiledetail("./sysconf/systeminfo.json");

                     $obj=json_decode($retarray,true);
                     $temp = array(
                        'parameter'=>$obj,
                        'configure'=>$panel,
                        'running'=> $retstatus
                     );
                    $retval=array(
                        'status'=>'true',
                        'auth'=>'true',
                        'ret'=>$temp,
                        'msg'=>''
                    );

                    $jsonencode = _encode($retval);
                    echo $jsonencode; break;
    case "ZH_Medicine_task_running":
        $body=$payload["body"];
        $panel = $body["configure"];
        $retstatus="true";
        $arrlength=count($panel["picture"]);
        //echo "picturelength:".(string)$arrlength;
        for($i=0;$i<$arrlength;$i++){

           // echo "$panel[picture][".(string)$i."][shooting]:".$panel["picture"][$i]["shooting"];
            if(0==strcmp($panel["picture"][$i]["shooting"],"false")){
                $panel["picture"][$i]["shooting"]="true";
                if(($i-1)>=0){
                    $panel["picture"][$i-1]["videoing"]="true";
                    $panel["picture"][$i-1]["shooting"]="done";
                    $shootnumber = rand(1,4);
                    $shootarray = array();
                    for($j=0;$j<$shootnumber;$j++){
                        array_push($shootarray,"./demo/pic/shoot".(string)($j+1).".png");
                    }
                    $panel["picture"][$i-1]["shoot"]=$shootarray;
                }
                if(($i-2)>=0){
                     $panel["picture"][$i-2]["videoing"]="done";
                     $panel["picture"][$i-2]["video"]="./demo/video/avorion.mp4";
                     $panel["picture"][$i-2]["shooting"]="done";
                     $panel["picture"][$i-2]["analysising"]="true";
                 }
                 if(($i-3)>=0){

                     $panel["picture"][$i-3]["videoing"]="done";
                     $panel["picture"][$i-3]["shooting"]="done";
                     $panel["picture"][$i-3]["analysising"]="done";
                     //$panel["picture"][$i-3]["analysis"]["resultPic"]="./demo/pic/result.png";
                     $panel["picture"][$i-3]["analysis"]["resultPic"]=array();
                     for($j=0;$j<count($panel["picture"][$i-3]["shoot"]);$j++){
                        array_push($panel["picture"][$i-3]["analysis"]["resultPic"],"./demo/pic/result.png");
                     }
                     $panel["picture"][$i-3]["analysis"]["result"]=array();
                     for($j=0;$j<5;$j++){
                        $resultitem=array(
                            'title'=>'result'.(string)$j,
                            'value'=>(string)rand(0,1000)
                        );
                        array_push($panel["picture"][$i-3]["analysis"]["result"],$resultitem);
                     }
                 }
                break;
            }
            if($i== ($arrlength-1)){
                if(0!=strcmp($panel["picture"][$i]["shooting"], "done")){
                    $panel["picture"][$i]["shooting"] = "done";
                    $panel["picture"][$i]["videoing"] = "true";
                    $shootnumber = rand(1,4);
                    $shootarray = array();
                    for($j=0;$j<$shootnumber;$j++){
                        array_push($shootarray,"./demo/pic/shoot".(string)($j+1).".png");
                    }
                    $panel["picture"][$i]["shoot"]=$shootarray;
                    if(($i-1)>=0){
                        $panel["picture"][$i-1]["videoing"]="done";
                        $panel["picture"][$i-1]["analysising"]="true";
                        $panel["picture"][$i-1]["video"]="./demo/video/avorion.mp4";
                    }
                    if(($i-2)>=0){
                        $panel["picture"][$i-2]["analysising"]="done";
                        //$panel["picture"][$i-2]["analysis"]["resultPic"]="./demo/pic/result.png";
                        $panel["picture"][$i-2]["analysis"]["resultPic"]=array();
                         for($j=0;$j<count($panel["picture"][$i-2]["shoot"]);$j++){
                            array_push($panel["picture"][$i-2]["analysis"]["resultPic"],"./demo/pic/result.png");
                         }
                         $panel["picture"][$i-2]["analysis"]["result"]=array();
                         for($j=0;$j<5;$j++){
                            $resultitem=array(
                                'title'=>'result'.(string)$j,
                                'value'=>(string)rand(0,1000)
                            );
                            array_push($panel["picture"][$i-2]["analysis"]["result"],$resultitem);
                         }
                    }
                }else if(0!=strcmp($panel["picture"][$i]["videoing"],"done")){
                    $panel["picture"][$i]["videoing"] = "done";
                        $panel["picture"][$i]["video"]="./demo/video/avorion.mp4";
                    $panel["picture"][$i]["analysising"]="true";
                    if(($i-1)>=0){
                        $panel["picture"][$i-1]["analysising"]="done";
                        //$panel["picture"][$i-1]["analysis"]["resultPic"]="./demo/pic/result.png";
                        $panel["picture"][$i-1]["analysis"]["resultPic"]=array();
                         for($j=0;$j<count($panel["picture"][$i-1]["shoot"]);$j++){
                            array_push($panel["picture"][$i-1]["analysis"]["resultPic"],"./demo/pic/result.png");
                         }
                         $panel["picture"][$i-1]["analysis"]["result"]=array();
                         for($j=0;$j<5;$j++){
                            $resultitem=array(
                                'title'=>'result'.(string)$j,
                                'value'=>(string)rand(0,1000)
                            );
                            array_push($panel["picture"][$i-1]["analysis"]["result"],$resultitem);
                         }
                    }
                }else{
                    $panel["picture"][$i]["analysising"]="done";
                    //$panel["picture"][$i]["analysis"]["resultPic"]="./demo/pic/result.png";
                    $panel["picture"][$i]["analysis"]["resultPic"]=array();
                     for($j=0;$j<count($panel["picture"][$i]["shoot"]);$j++){
                        array_push($panel["picture"][$i]["analysis"]["resultPic"],"./demo/pic/result.png");
                     }
                     $panel["picture"][$i]["analysis"]["result"]=array();
                     for($j=0;$j<5;$j++){
                        $resultitem=array(
                            'title'=>'result'.(string)$j,
                            'value'=>(string)rand(0,1000)
                        );
                        array_push($panel["picture"][$i]["analysis"]["result"],$resultitem);
                     }
                    $retstatus = "false";
                }
            }


        }
                    $retarray;
                    $retarray = getfiledetail("./sysconf/systeminfo.json");

                     $obj=json_decode($retarray,true);
                     $temp = array(
                        'parameter'=>$obj,
                        'configure'=>$panel,
                        'running'=> $retstatus
                     );
                    $retval=array(
                        'status'=>'true',
                        'auth'=>'true',
                        'ret'=>$temp,
                        'msg'=>''
                    );

                    $jsonencode = _encode($retval);
                    echo $jsonencode; break;
    
    case "ZH_Medicine_set_temp_conf":
        $body=$payload["body"];

        tempmod(_encode($body));
        $retval=array(
            'status'=>'true',
            'auth'=>'true',
            'ret'=>$body,
            'msg'=>''
        );
        $jsonencode = _encode($retval);
        echo $jsonencode; break;
    case "ZH_Medicine_get_temp_conf":

        $retarray = getfiledetail("./sysconf/IdentifyParameter.json");
        $obj=json_decode($retarray,true);
        $retval=array(
            'status'=>'true',
            'auth'=>'true',
            'ret'=>$obj,
            'msg'=>''
        );
        $jsonencode = _encode($retval);
        echo $jsonencode; break;
    case "ZH_Medicine_run_temp_analysis":
        $body=$payload["body"];
        tempmod(_encode($body));
        $retval=array(
            'status'=>'true',
            'auth'=>'true',
            'ret'=>$body,
            'msg'=>''
        );
        $jsonencode = _encode($retval);
        echo $jsonencode; break;
    case "ZH_Medicine_get_temp_task_status":
        $body=$payload["body"];
        $body['analysis']['result']=array();
        $temp = array(
        'title'=> "temptrain",
        'value'=>"true"
        );
        array_push($body['analysis']['result'],$temp);
        $iffinish = rand(1,20);
        $temp;
        if($iffinish <=15){
            $temp=array(
                'status'=>'false'
            );
        }else{
            $temp=array(
                'status'=>'true',
                'result'=>$body
            );
        }
        $msgnote = rand(0,100);
        $retval=array(
            'status'=>'true',
            'ret'=>$temp,
            'auth'=>'true',
            'msg'=>'process'.(string)$msgnote."%"
        );
        $jsonencode = _encode($retval);
        echo $jsonencode; break;
    case "ZH_Medicine_save_temp_conf":
        $body=$payload["body"];

        tempmod(_encode($body));
        $retval=array(
            'status'=>'true',
            'auth'=>'true',
            'msg'=>''
        );
        $jsonencode = _encode($retval);
        echo $jsonencode; break;


        case "ZH_Medicine_sys_config":
            $retarray;
            $retarray = getfiledetail("./sysconf/configure.json");
            //$retarray = icon_to_utf8($retarray);
            //echo "file content".$retarray;
            $obj=json_decode($retarray,true);
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'ret'=>$obj,
                'msg'=>''
            );

            $jsonencode = _encode($retval);

            echo $jsonencode; break;
        case "ZH_Medicine_sys_debug":
            break;
        case "ZH_Medicine_export":
            break;
        case "ZH_Medicine_sys_config_save":
            $body=$payload["body"];
            $sta='true';
            confmod(_encode($body));
                $retval=array(
                    'status'=>$sta,
                    'auth'=>'true',
                    'msg'=>'12345'
                );

                $jsonencode = _encode($retval);
                echo $jsonencode; break;
        case "ZH_Medicine_sys_debug_run":
            break;
        case "ZH_Medicine_export_run":
            break;


        case "ZH_Medicine_sys_language":
            $body=$payload["body"];
            $defaultlanguage = $body["default"];
            languagemod(_encode($body));
            $retarray = getfiledetail("./language/language_".$defaultlanguage.".json");
            //echo "file content".$retarray;
            $obj=json_decode($retarray,true);
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'ret'=>$obj,
                'msg'=>''
            );

            $jsonencode = _encode($retval);

            echo $jsonencode; break;
        case "ZH_Medicine_sys_language_list":
            $retarray;
            $retarray = getfiledetail("./sysconf/supportlanguage.json");
            //echo "file content".$retarray;
            $obj=json_decode($retarray,true);
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'ret'=>$obj,
                'msg'=>''
            );

            $jsonencode = _encode($retval);

            echo $jsonencode; break;
        case "ZH_Medicine_sys_version":
            break;
        case "ZH_Medicine_change_passwd":
            $body=$payload["body"];
            $username = $body["username"];
            $password = $body["password"];
            $newpassword = $body["newpassword"];
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'msg'=>''
            );
            $jsonencode = _encode($retval);
            echo $jsonencode; break;
        case "ZH_Medicine_get_user_list":
            $userlist=array();
            for($i=0;$i<20;$i++){
                $temp="user".(string)$i;
                array_push($userlist,$temp);
            }
            $retval=array(
                'ret'=>$userlist,
                'status'=>'true',
                'auth'=>'true',
                'msg'=>''
            );
            $jsonencode = _encode($retval);
            echo $jsonencode; break;
        case "ZH_Medicine_del_user":
            $body=$payload["body"];
            $user = $body["username"];
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'msg'=>''
            );
            $jsonencode = _encode($retval);
            echo $jsonencode; break;
        case "ZH_Medicine_new_user":
            $body=$payload["body"];
            $user = $body["username"];
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'msg'=>''
            );
            $jsonencode = _encode($retval);
            echo $jsonencode; break;
        case "ZH_Medicine_reset_user":
            $body=$payload["body"];
            $user = $body["username"];
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'msg'=>''
            );
            $jsonencode = _encode($retval);
            echo $jsonencode; break;
        case "ZH_Medicine_mqtt_conf":
            $retarray = getfiledetail("./sysconf/mqtt.json");
            //echo "file content".$retarray;
            $obj=json_decode($retarray,true);
            $retval=array(
                'status'=>'true',
                'auth'=>'true',
                'ret'=>$obj,
                'msg'=>''
            );

            $jsonencode = _encode($retval);

            echo $jsonencode; break;
	default:

	break;
}
function calizero(){
    $server = "127.0.0.1";     // change if necessary
    $port = 1883;                     // change if necessary
    $username = "";                   // set your username
    $password = "";                   // set your password
    $client_id = "MQTT_XH_High_Speed_Balance_PHP"; // make sure this is unique for connecting to sever - you could use uniqid()
    $mqtt = new phpMQTT($server, $port, $client_id);
    if(!$mqtt->connect(true, NULL, $username, $password)) {
        exit(1);
    }
    $topics['MQTT_XH_High_Speed_Balance_PHP'] = array("qos" => 0, "function" => "procmsg");
    //$mqtt->subscribe($topics, 0);
    $retval=array(
                       'action'=>'XH_High_Speed_Balance_calibration_zero_trigger'
                   );

    $mqtt->publish('MQTT_XH_High_Speed_Balance_HCU', _encode($retval));

    $mqtt->close();
}
function caliweight(){
    $server = "127.0.0.1";     // change if necessary
    $port = 1883;                     // change if necessary
    $username = "";                   // set your username
    $password = "";                   // set your password
    $client_id = "MQTT_XH_High_Speed_Balance_PHP"; // make sure this is unique for connecting to sever - you could use uniqid()
    $mqtt = new phpMQTT($server, $port, $client_id);
    if(!$mqtt->connect(true, NULL, $username, $password)) {
        exit(1);
    }
    $topics['MQTT_XH_High_Speed_Balance_PHP'] = array("qos" => 0, "function" => "procmsg");
    //$mqtt->subscribe($topics, 0);
    $retval=array(
                       'action'=>'XH_High_Speed_Balance_calibration_weight_trigger'
                   );

    $mqtt->publish('MQTT_XH_High_Speed_Balance_HCU', _encode($retval));

    $mqtt->close();
}
function calidynamic($bool){
    $server = "127.0.0.1";     // change if necessary
    $port = 1883;                     // change if necessary
    $username = "";                   // set your username
    $password = "";                   // set your password
    $client_id = "MQTT_XH_High_Speed_Balance_PHP"; // make sure this is unique for connecting to sever - you could use uniqid()
    $mqtt = new phpMQTT($server, $port, $client_id);
    if(!$mqtt->connect(true, NULL, $username, $password)) {
        exit(1);
    }
    $topics['MQTT_XH_High_Speed_Balance_PHP'] = array("qos" => 0, "function" => "procmsg");
    //$mqtt->subscribe($topics, 0);
    $action = 'XH_High_Speed_Balance_calibration_dynamic_stop';
    if($bool) $action = 'XH_High_Speed_Balance_calibration_dynamic_start';
    $retval=array(
                       'action'=>$action
                   );

    $mqtt->publish('MQTT_XH_High_Speed_Balance_HCU', _encode($retval));

    $mqtt->close();
}
function flushUI(){
    $server = "127.0.0.1";     // change if necessary
    $port = 1883;                     // change if necessary
    $username = "";                   // set your username
    $password = "";                   // set your password
    $client_id = "MQTT_XH_High_Speed_Balance_PHP"; // make sure this is unique for connecting to sever - you could use uniqid()
    $mqtt = new phpMQTT($server, $port, $client_id);
    if(!$mqtt->connect(true, NULL, $username, $password)) {
        exit(1);
    }
    $topics['MQTT_XH_High_Speed_Balance_PHP'] = array("qos" => 0, "function" => "procmsg");
    //$mqtt->subscribe($topics, 0);
    $retval=array(
                       'action'=>'XH_High_Speed_Balance_force_flush'
                   );

    $mqtt->publish('MQTT_XH_High_Speed_Balance_HCU', _encode($retval));

    $mqtt->close();
}

function runpause(){
     $server = "127.0.0.1";     // change if necessary
     $port = 1883;                     // change if necessary
     $username = "";                   // set your username
     $password = "";                   // set your password
     $client_id = "MQTT_XH_High_Speed_Balance_PHP"; // make sure this is unique for connecting to sever - you could use uniqid()
     $mqtt = new phpMQTT($server, $port, $client_id);
     if(!$mqtt->connect(true, NULL, $username, $password)) {
         exit(1);
     }
     $topics['MQTT_XH_High_Speed_Balance_PHP'] = array("qos" => 0, "function" => "procmsg");
     //$mqtt->subscribe($topics, 0);
     $retval=array(
                        'action'=>'XH_High_Speed_Balance_pause_trigger'
                    );

     $mqtt->publish('MQTT_XH_High_Speed_Balance_HCU', _encode($retval));

     $mqtt->close();
}
function runresume(){
    $server = "127.0.0.1";     // change if necessary
    $port = 1883;                     // change if necessary
    $username = "";                   // set your username
    $password = "";                   // set your password
    $client_id = "MQTT_XH_High_Speed_Balance_PHP"; // make sure this is unique for connecting to sever - you could use uniqid()
    $mqtt = new phpMQTT($server, $port, $client_id);
    if(!$mqtt->connect(true, NULL, $username, $password)) {
        exit(1);
    }
    $topics['MQTT_XH_High_Speed_Balance_PHP'] = array("qos" => 0, "function" => "procmsg");
    //$mqtt->subscribe($topics, 0);
    $retval=array(
                       'action'=>'XH_High_Speed_Balance_resume_trigger'
                   );

    $mqtt->publish('MQTT_XH_High_Speed_Balance_HCU', _encode($retval));

    $mqtt->close();
}


class phpMQTT {
	private $socket; 			/* holds the socket	*/
	private $msgid = 1;			/* counter for message id */
	public $keepalive = 10;		/* default keepalive timmer */
	public $timesinceping;		/* host unix time, used to detect disconects */
	public $topics = array(); 	/* used to store currently subscribed topics */
	public $debug = false;		/* should output debug messages */
	public $address;			/* broker address */
	public $port;				/* broker port */
	public $clientid;			/* client id sent to brocker */
	public $will;				/* stores the will of the client */
	private $username;			/* stores username */
	private $password;			/* stores password */
	public $cafile;
	function __construct($address, $port, $clientid, $cafile = NULL){
		$this->broker($address, $port, $clientid, $cafile);
	}
	/* sets the broker details */
	function broker($address, $port, $clientid, $cafile = NULL){
		$this->address = $address;
		$this->port = $port;
		$this->clientid = $clientid;
		$this->cafile = $cafile;
	}
	function connect_auto($clean = true, $will = NULL, $username = NULL, $password = NULL){
		while($this->connect($clean, $will, $username, $password)==false){
			sleep(10);
		}
		return true;
	}
	/* connects to the broker
		inputs: $clean: should the client send a clean session flag */
	function connect($clean = true, $will = NULL, $username = NULL, $password = NULL){

		if($will) $this->will = $will;
		if($username) $this->username = $username;
		if($password) $this->password = $password;
		if ($this->cafile) {
			$socketContext = stream_context_create(["ssl" => [
				"verify_peer_name" => true,
				"cafile" => $this->cafile
				]]);
			$this->socket = stream_socket_client("tls://" . $this->address . ":" . $this->port, $errno, $errstr, 60, STREAM_CLIENT_CONNECT, $socketContext);
		} else {
			$this->socket = stream_socket_client("tcp://" . $this->address . ":" . $this->port, $errno, $errstr, 60, STREAM_CLIENT_CONNECT);
		}
		if (!$this->socket ) {
		    if($this->debug) error_log("stream_socket_create() $errno, $errstr \n");
			return false;
		}
		stream_set_timeout($this->socket, 5);
		stream_set_blocking($this->socket, 0);
		$i = 0;
		$buffer = "";
		$buffer .= chr(0x00); $i++;
		$buffer .= chr(0x06); $i++;
		$buffer .= chr(0x4d); $i++;
		$buffer .= chr(0x51); $i++;
		$buffer .= chr(0x49); $i++;
		$buffer .= chr(0x73); $i++;
		$buffer .= chr(0x64); $i++;
		$buffer .= chr(0x70); $i++;
		$buffer .= chr(0x03); $i++;
		//No Will
		$var = 0;
		if($clean) $var+=2;
		//Add will info to header
		if($this->will != NULL){
			$var += 4; // Set will flag
			$var += ($this->will['qos'] << 3); //Set will qos
			if($this->will['retain'])	$var += 32; //Set will retain
		}
		if($this->username != NULL) $var += 128;	//Add username to header
		if($this->password != NULL) $var += 64;	//Add password to header
		$buffer .= chr($var); $i++;
		//Keep alive
		$buffer .= chr($this->keepalive >> 8); $i++;
		$buffer .= chr($this->keepalive & 0xff); $i++;
		$buffer .= $this->strwritestring($this->clientid,$i);
		//Adding will to payload
		if($this->will != NULL){
			$buffer .= $this->strwritestring($this->will['topic'],$i);
			$buffer .= $this->strwritestring($this->will['content'],$i);
		}
		if($this->username) $buffer .= $this->strwritestring($this->username,$i);
		if($this->password) $buffer .= $this->strwritestring($this->password,$i);
		$head = "  ";
		$head{0} = chr(0x10);
		$head{1} = chr($i);
		fwrite($this->socket, $head, 2);
		fwrite($this->socket,  $buffer);
	 	$string = $this->read(4);
		if(ord($string{0})>>4 == 2 && $string{3} == chr(0)){
			if($this->debug) echo "Connected to Broker\n";
		}else{
			error_log(sprintf("Connection failed! (Error: 0x%02x 0x%02x)\n",
			                        ord($string{0}),ord($string{3})));
			return false;
		}
		$this->timesinceping = time();
		return true;
	}
	/* read: reads in so many bytes */
	function read($int = 8192, $nb = false){
		//	print_r(socket_get_status($this->socket));

		$string="";
		$togo = $int;

		if($nb){
			return fread($this->socket, $togo);
		}

		while (!feof($this->socket) && $togo>0) {
			$fread = fread($this->socket, $togo);
			$string .= $fread;
			$togo = $int - strlen($string);
		}




			return $string;
	}
	/* subscribe: subscribes to topics */
	function subscribe($topics, $qos = 0){
		$i = 0;
		$buffer = "";
		$id = $this->msgid;
		$buffer .= chr($id >> 8);  $i++;
		$buffer .= chr($id % 256);  $i++;
		foreach($topics as $key => $topic){
			$buffer .= $this->strwritestring($key,$i);
			$buffer .= chr($topic["qos"]);  $i++;
			$this->topics[$key] = $topic;
		}
		$cmd = 0x80;
		//$qos
		$cmd +=	($qos << 1);
		$head = chr($cmd);
		$head .= chr($i);

		fwrite($this->socket, $head, 2);
		fwrite($this->socket, $buffer, $i);
		$string = $this->read(2);

		$bytes = ord(substr($string,1,1));
		$string = $this->read($bytes);
	}
	/* ping: sends a keep alive ping */
	function ping(){
			$head = " ";
			$head = chr(0xc0);
			$head .= chr(0x00);
			fwrite($this->socket, $head, 2);
			if($this->debug) echo "ping sent\n";
	}
	/* disconnect: sends a proper disconect cmd */
	function disconnect(){
			$head = " ";
			$head{0} = chr(0xe0);
			$head{1} = chr(0x00);
			fwrite($this->socket, $head, 2);
	}
	/* close: sends a proper disconect, then closes the socket */
	function close(){
	 	$this->disconnect();
		stream_socket_shutdown($this->socket, STREAM_SHUT_WR);
	}
	/* publish: publishes $content on a $topic */
	function publish($topic, $content, $qos = 0, $retain = 0){
		$i = 0;
		$buffer = "";
		$buffer .= $this->strwritestring($topic,$i);
		//$buffer .= $this->strwritestring($content,$i);
		if($qos){
			$id = $this->msgid++;
			$buffer .= chr($id >> 8);  $i++;
		 	$buffer .= chr($id % 256);  $i++;
		}
		$buffer .= $content;
		$i+=strlen($content);
		$head = " ";
		$cmd = 0x30;
		if($qos) $cmd += $qos << 1;
		if($retain) $cmd += 1;
		$head{0} = chr($cmd);
		$head .= $this->setmsglength($i);
		fwrite($this->socket, $head, strlen($head));
		fwrite($this->socket, $buffer, $i);
	}
	/* message: processes a recieved topic */
	function message($msg){
		 	$tlen = (ord($msg{0})<<8) + ord($msg{1});
			$topic = substr($msg,2,$tlen);
			$msg = substr($msg,($tlen+2));
			$found = 0;
			foreach($this->topics as $key=>$top){
				if( preg_match("/^".str_replace("#",".*",
						str_replace("+","[^\/]*",
							str_replace("/","\/",
								str_replace("$",'\$',
									$key))))."$/",$topic) ){
					if(is_callable($top['function'])){
						call_user_func($top['function'],$topic,$msg);
						$found = 1;
					}
				}
			}
			if($this->debug && !$found) echo "msg recieved but no match in subscriptions\n";
	}
	/* proc: the processing loop for an "allways on" client
		set true when you are doing other stuff in the loop good for watching something else at the same time */
	function proc( $loop = true){
		if(1){
			$sockets = array($this->socket);
			$w = $e = NULL;
			$cmd = 0;

				//$byte = fgetc($this->socket);
			if(feof($this->socket)){
				if($this->debug) echo "eof receive going to reconnect for good measure\n";
				fclose($this->socket);
				$this->connect_auto(false);
				if(count($this->topics))
					$this->subscribe($this->topics);
			}

			$byte = $this->read(1, true);

			if(!strlen($byte)){
				if($loop){
					usleep(100000);
				}

			}else{

				$cmd = (int)(ord($byte)/16);
				if($this->debug) echo "Recevid: $cmd\n";
				$multiplier = 1;
				$value = 0;
				do{
					$digit = ord($this->read(1));
					$value += ($digit & 127) * $multiplier;
					$multiplier *= 128;
					}while (($digit & 128) != 0);
				if($this->debug) echo "Fetching: $value\n";

				if($value)
					$string = $this->read($value);

				if($cmd){
					switch($cmd){
						case 3:
							$this->message($string);
						break;
					}
					$this->timesinceping = time();
				}
			}
			if($this->timesinceping < (time() - $this->keepalive )){
				if($this->debug) echo "not found something so ping\n";
				$this->ping();
			}

			if($this->timesinceping<(time()-($this->keepalive*2))){
				if($this->debug) echo "not seen a package in a while, disconnecting\n";
				fclose($this->socket);
				$this->connect_auto(false);
				if(count($this->topics))
					$this->subscribe($this->topics);
			}
		}
		return 1;
	}
	/* getmsglength: */
	function getmsglength(&$msg, &$i){
		$multiplier = 1;
		$value = 0 ;
		do{
		  $digit = ord($msg{$i});
		  $value += ($digit & 127) * $multiplier;
		  $multiplier *= 128;
		  $i++;
		}while (($digit & 128) != 0);
		return $value;
	}
	/* setmsglength: */
	function setmsglength($len){
		$string = "";
		do{
		  $digit = $len % 128;
		  $len = $len >> 7;
		  // if there are more digits to encode, set the top bit of this digit
		  if ( $len > 0 )
		    $digit = ($digit | 0x80);
		  $string .= chr($digit);
		}while ( $len > 0 );
		return $string;
	}
	/* strwritestring: writes a string to a buffer */
	function strwritestring($str, &$i){
		$ret = " ";
		$len = strlen($str);
		$msb = $len >> 8;
		$lsb = $len % 256;
		$ret = chr($msb);
		$ret .= chr($lsb);
		$ret .= $str;
		$i += ($len+2);
		return $ret;
	}
	function printstr($string){
		$strlen = strlen($string);
			for($j=0;$j<$strlen;$j++){
				$num = ord($string{$j});
				if($num > 31)
					$chr = $string{$j}; else $chr = " ";
				printf("%4d: %08b : 0x%02x : %s \n",$j,$num,$num,$chr);
			}
	}

}
?>