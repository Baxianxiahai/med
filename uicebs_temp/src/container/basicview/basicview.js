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
import '../../../resource/css/font-awesome.min.css';

import Locationcard from "../cards/locationcard/location"
import Panelcard from "../cards/panelcard/panel"
import Localpicturecard from "../cards/localpicturecard/localpicture"
import Realpicturecard from "../cards/realpicturecard/realpicture"
import Parametercard from "../cards/parametercard/parameter"
import Taskcard from "../cards/taskcard/task"
import Resultviewcard from "../cards/resultviewcard/resultview"



require('es6-promise').polyfill();
export default class basicview extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            leftview: null,
            rightview:null,
            hide:"block",
            callback:null,
            margintop:20,
            language:{
            }
        }
        //this.keyboard_initialize();

        this._taskcallbackreset=this.reset_panel.bind(this);
        this._taskgetbatchinfo=this.get_batch_info.bind(this);
        this._showresult=this.update_result.bind(this);
    }
    update_language(language){
        this.setState({language:language});
        this.refs.Parametercard.update_language(language.parameter);
        this.refs.Taskcard.update_language(language.task);
        this.refs.Panelcard.update_language(language.panel);
        this.refs.Resultviewcard.update_language(language.result);
    }

    initializeparameter(callback,configure){
        this.refs.Parametercard.update_callback(callback);
        this.refs.Parametercard.update_config(configure);
    }
    update_size(width,height){
        this.setState({height:height,width:width});
        this.refs.Locationcard.update_size(parseInt(width/2),height,0);
        this.refs.Parametercard.update_size(parseInt(width),height,0);
        this.refs.Taskcard.update_size(parseInt(width/4),height,0);
        this.refs.Panelcard.update_size(width-parseInt(width/4),height,0);
        this.refs.Localpicturecard.update_size(width-parseInt(width/2),height,0);
        this.refs.Realpicturecard.update_size(width-parseInt(width/2),height,0);
        this.refs.Resultviewcard.update_size(width,height,0);
    }
    update_result(result){

        this.refs.Resultviewcard.update_content(result);
        //this.refs.Resultviewcard.show();
    }
    update_panel(configure){
        this.refs.Panelcard.update_configure(configure);
    }
    get_current_panel_configure(){
        return this.refs.Panelcard.get_configure();
    }
    get_running(){
        return this.refs.Taskcard.get_running();
    }
    getsysconfset(){
        return this.refs.Parametercard.getUpdatedValue();
    }
    reset_panel(){
        let temp = this.refs.Panelcard.get_configure()
        for(let i =0; i < temp.picture.length;i++){
            temp.picture[i].shoot=[];
            temp.picture[i].video="";
            temp.picture[i].shooting="false";
            temp.picture[i].videoing="false";
            temp.picture[i].analysising="false";
        }
        temp.basic.analysis="false";
        temp.basic.video = "false";
        temp.basic.batch="";

        this.refs.Panelcard.update_configure(temp);
        this.refs.Taskcard.update_configure_panel(temp);
        this.refs.Panelcard.change_status("choice");
    }
    update_task(task){
        this.refs.Taskcard.update_configure(task);
        this.refs.Panelcard.update_configure(task.configure);
        if(task.running==="true"){
            console.log("change to run status");
            this.handle_running();
        }else{
            if(task.configure.basic.batch === ""){

                console.log("change to reset status");
                this.refs.Panelcard.change_status("choice");
            }else{

                console.log("change to view status");
                this.handle_stop();
            }
            //
        }
    }
    update_task_callback(callback,foot,callbacksave){
        this.refs.Taskcard.update_callback(callback,foot);
        this.refs.Parametercard.update_callback_save(callbacksave);
    }
    update_result_callback(gettemp,savetemp,runtemp){
        this.refs.Resultviewcard.update_callback(gettemp,savetemp,runtemp);
    }
    handle_running(){
        //this.refs.Panelcard.show_index(false);
        //this.refs.Panelcard.disable_button(true);
        this.refs.Panelcard.change_status("running");
    }
    handle_stop(){
        //this.refs.Panelcard.show_index(true);
        //this.refs.Panelcard.disable_button(false);
        this.refs.Panelcard.change_status("view");
    }
    get_batch_info(){
        return this.refs.Panelcard.get_batch_info();
    }
    get_result_content(){
        return this.refs.Resultviewcard.get_content();
    }
    Resultviewcard(){
        return this.refs.Resultviewcard;
    }
    hide(){
        this.setState({hide:"none"});
    }
    show(){
        this.setState({hide:"block"});

    }

    componentDidMount(){
    }
    componentDidUpdate(){
    }
    clearview(){
        this.props.basiccallbacklockfoot(true);
        this.refs.Taskcard.hide();
        this.refs.Localpicturecard.hide();
        this.refs.Parametercard.hide();
        this.refs.Locationcard.hide();
        this.refs.Panelcard.hide();
        this.refs.Realpicturecard.hide();
        this.refs.Resultviewcard.hide();
    }
    taskview(){
        this.clearview();
        let localitem = this;
        setTimeout(function(){
            localitem.refs.Taskcard.show();
            localitem.refs.Panelcard.show();
            localitem.props.basiccallbacklockfoot(false);
        },900);


    }
    parameterview(){
        this.clearview();
        let localitem = this;
        setTimeout(function(){
            localitem.refs.Parametercard.show();
            //localitem.refs.Localpicturecard.show();
            localitem.props.basiccallbacklockfoot(false);
        },900);


        /*
        this.clearview();
        this.refs.Parametercard.show();
        this.refs.Picturecard.show();
        return new Promise((resolve) => {
            this.setState({leftview:this.refs.Parametercard,right:this.refs.Picturecard}, resolve)
        });*/

    }
    locationview(){
        this.clearview();

        let localitem = this;
        setTimeout(function(){

            localitem.refs.Locationcard.show();
            localitem.refs.Realpicturecard.show();
            localitem.props.basiccallbacklockfoot(false);
        },900);

        /*
        this.clearview();
        this.refs.Locationcard.show();
        this.refs.Picturecard.show();
        return new Promise((resolve) => {
            this.setState({leftview:this.refs.Locationcard,right:this.refs.Picturecard}, resolve)
        });*/
    }
    updatetempconf(conf){
        this.refs.Resultviewcard.updatetempconf(conf);
    }
    render() {
        return (
            <div className="loginbackground" style={{position:"relative",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:'100%',display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',backgroundImage: "url(./resource/image/zhihe2.png)"
                ,backgroundRepeat:"no-repeat",backgroundSize:"100% 100%",MozBackgroundSize:"100% 100%"}}>

                    <Locationcard ref="Locationcard" basiccallbacklockfoot = {this.props.basiccallbacklockfoot}/>
                    <Parametercard ref="Parametercard" basiccallbacklockfoot = {this.props.basiccallbacklockfoot}/>
                    <Taskcard ref="Taskcard" basiccallbacklockfoot = {this.props.basiccallbacklockfoot}
                              taskcallbackreset={this._taskcallbackreset}/>
                    <Panelcard ref="Panelcard" basiccallbacklockfoot = {this.props.basiccallbacklockfoot}
                    showresult={this._showresult}/>
                    <Localpicturecard ref="Localpicturecard" basiccallbacklockfoot = {this.props.basiccallbacklockfoot}/>
                    <Realpicturecard ref="Realpicturecard" basiccallbacklockfoot = {this.props.basiccallbacklockfoot}/>
                    <Resultviewcard ref="Resultviewcard"
                                    basiccallbacklockfoot = {this.props.basiccallbacklockfoot}
                    />

            </div>
        );
    }
}