/**
 * Created by Huang Yuanjie on 2019/1/5.
 */
/**
 * Created by hyj on 2016/12/22.
 */

/**
 * Created by hyj on 2016/9/29.
 */
import React, {
    Component,
    PropTypes
} from 'react';

import classNames from 'classnames';
import '../../../../resource/css/font-awesome.min.css';



export default class taskcard extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            margin:75,
            hide:"none",
            animate:"animated fadeInLeft",
            callback:null,
            footcallback:null,
            margintop:20,
            disabled:"",
            disabledreset:"",
            key:"taskinfo",
            parameter:[
                {"title":"状态1","value":"123","alarm":false},
                {"title":"状态2","value":"123","alarm":false},
                {"title":"状态3","value":"123","alarm":false},
                {"title":"状态4","value":"123","alarm":false},
                {"title":"状态5","value":"123","alarm":false},
                {"title":"状态6","value":"123","alarm":false},
                {"title":"状态7","value":"123","alarm":false}
            ],
            configure:null,
            running:false,

            language:{
                "taskparameter":"识别参数",
                "taskinfo":"任务信息",
                "consoletitle":"实时日志",
                "start":"开始",
                "stop":"停止",
                "reset":"重置状态"
            }
        }
    }
    update_language(language){
        this.setState({language:language});
    }
    update_size(width,height,margin){
        this.setState({height:height,width:width,margin:margin});
    }
    get_batch_info(){
        if(this.state.configure === null) return [];
        else{
            let temp = [];
            temp.push({
                "title":this.state.language.batch,
                "value":this.state.configure.basic.batch
            });
            temp.push({
                "title":this.state.language.date,
                "value":this.state.configure.basic.date
            });
            temp.push({
                "title":this.state.language.owner,
                "value":this.state.configure.basic.owner
            });
            temp.push({
                "title":this.state.language.tupid,
                "value":this.state.configure.basic.tupid
            });
            for(let i=0; i < this.state.configure.basic.extra.length;i++){
                temp.push(this.state.configure.basic.extra[i]);
            }
            return temp;
        }
    }
    update_configure(task){
        let x = false;
        if(task.running==="true"){
            console.log("task set running true");
            this.props.basiccallbacklockfoot(true);
            x=true;
        }
        else this.props.basiccallbacklockfoot(false);
        this.setState({parameter:task.parameter.info,running:x,configure:task.configure});
    }
    update_configure_panel(configure){
        this.setState({configure:configure});
    }
    update_callback(callback,footcallback){
        this.setState({callback:callback,footcallback:footcallback});
    }
    set_running(bool){
        if(bool){
            this.setState({running:true,disabledreset:"disabled"});
        }else
            this.setState({running:false,disabledreset:""});
    }
    get_running(){
        return this.state.running;
    }
    hide(){
        if(this.state.hide === "none") return;
        else{
            this.setState({animate:"animated fadeOutLeft"});
            let self = this;
            setTimeout(function(){
                self.setState({hide:"none"});
            },800);
        }
        //this.setState({hide:"none"});
    }
    show(){
        //this.setState({hide:"block"});
        if(this.state.hide === "block") return;
        else{
            this.setState({hide:"block",animate:"animated fadeInLeft"});
        }
    }
    switch_system_info(){
        if(this.state.hide == "none"){
            this.setState({hide:"block",animate:"animated fadeInLeft"});
        }else{
            this.setState({animate:"animated fadeOutleft"});
            let self = this;
            setTimeout(function(){
                self.setState({hide:"none"});
            },800);
        }
    }
    handle_click(){
        this.setState({disabled:"disabled"});
        if(this.get_running()){
            this.state.callback(false);
        }else{
            this.state.callback(true);
        }
        let temp = this;
        setTimeout(function(){
            temp.setState({disabled:""});
        },500);
        //console.log("click start button");
    }
    handle_reset(){
        //console.log("click reset button");
        this.props.taskcallbackreset();
    }
    render() {
        let center_panel=[];
        for(let i=0;i<this.state.parameter.length;i++){
            let temp = <h3 style={{fontSize:15,marginRight:5,color:"#333"}}  key={this.state.key+i}>{this.state.parameter[i].title+":"+this.state.parameter[i].value}</h3>
            if(this.state.parameter[i].alarm)
                temp = <h3 style={{fontSize:15,marginRight:5,color:"#FF6633"}}  key={this.state.key+i}>{this.state.parameter[i].title+":"+this.state.parameter[i].value}</h3>
            center_panel.push(temp);
        }
        let button_text = this.state.language.start;
        let task_information =[];
        if(this.state.configure!= null && this.state.configure.basic.batch != ""){
            let task_detai=[];
            let info_list = this.get_batch_info();
            for(let i=0;i<info_list.length;i++){
                let temp = <h3 style={{fontSize:15,marginRight:5,color:"#333"}}  key={this.state.key+i}>{this.state.parameter[i].title+":"+this.state.parameter[i].value}</h3>
                task_detai.push(temp);
            }
            task_information=
                <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key="status-second">
                    <div className="tile-stats"  style={{marginTop:"15px"}}>
                        <div className="count" style={{fontSize:24}}>{this.state.language.taskinfo}</div>
                        {task_detai}
                    </div>
                </div>
        }
        if(this.state.running) button_text = this.state.language.stop;
        return (
            <div className={this.state.animate} style={{position:"absolute",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:this.state.width,top:0,left:0,display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',zIndex:"99"}}>
                <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key="status-top">
                    <div className="tile-stats"  style={{marginTop:"15px"}}>
                        <div className="count" style={{fontSize:24}}>{this.state.language.taskparameter}</div>
                        {center_panel}
                    </div>
                </div>
                {task_information}
                <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key="status-bottom">
                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:(this.state.width*0.1-5),marginTop:"5px",height:(this.state.width-10)*0.2,width:(this.state.width-10)*0.8}} disabled={this.state.disabled} onClick={this.handle_click.bind(this)}>
                        <i style={{fontSize:25}}> {button_text}</i>
                    </button>
                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:(this.state.width*0.1-5),marginTop:"5px",height:(this.state.width-10)*0.2,width:(this.state.width-10)*0.8}} disabled={this.state.disabledreset} onClick={this.handle_reset.bind(this)}>
                        <i style={{fontSize:25}}> {this.state.language.reset}</i>
                    </button>
                </div>
            </div>
        );
    }
}