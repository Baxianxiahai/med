/**
 * Created by hyj on 2016/9/28.
 */
import React, {
    Component,
    PropTypes
    } from 'react';
/*
 import {
 AppRegistry,
 StyleSheet,
 Text,
 View,
 PixelRatio
 } from 'react-native';*/
import classNames from 'classnames';
import '../../resource/css/font-awesome.min.css';
import './foot.css';

export default class foot extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:50,
            content:"",

            hideReturn:"none",
            hideLanguage:"none",
            hideTask:"none",
            hideParameter:"none",
            hideLocation:"none",
            hideHistory:"none",
            hideAudit:"none",
            hideSystemInfo:"block",
            disabled:"",
            systeminfo:"",
            loginfo:"xxxxxxxxx",
            icon:"fa fa-angle-double-left",
            language:{
                "content":"",
                "getting":"Getting......",
                "upgrade":"System upgrade, new version:",
                "pnotifytitle":"System message:"
            }
        }
    }
    updateversion(version){

        this.setState({version:version});
        /*
        if(this.state.version.HCU == version.HCU &&this.state.version.IHU == version.IHU){
            return;
        }else{
            if(this.state.version.HCU == "Getting" || this.state.version.IHU == "Getting"){
                this.setState({version:version});
                this.closePnotify();
            }else{
                this.closePnotify();
                this.setState({version:version},this.openPnotifyupgrade);
            }
        }*/
    }
    update_language(language){
        this.setState({language:language});
    }
    write_log(log){
        if(log===undefined){
            return;
        }
        let loginfo=log;
        if(log.length>20){
            loginfo=log.substring(0,20)+"...";
        }
        this.setState({loginfo:loginfo});
    }
    update_size(height){
        this.setState({height:height})
    }
    update_content(content){
        let local =content;
        if(local.length>56) local=local.substr(0,56);
        this.setState({content:local});
    }



    show_return_button(input){
        if(input===true){
            this.setState({hideReturn:"block"});}
        else{
            this.setState({hideReturn:"none"});
        }
    }
    show_language_button(input){
        if(input===true){
            this.setState({hideLanguage:"block"});}
        else{
            this.setState({hideLanguage:"none"});
        }
    }
    show_task_button(input){
        if(input===true){
            this.setState({hideTask:"block"});}
        else{
            this.setState({hideTask:"none"});
        }
    }
    show_parameter_button(input){
        if(input===true){
            this.setState({hideParameter:"block"});}
        else{
            this.setState({hideParameter:"none"});
        }
    }
    show_location_button(input){
        if(input===true){
            this.setState({hideLocation:"block"});}
        else{
            this.setState({hideLocation:"none"});
        }
    }
    show_history_button(input){
        if(input===true){
            this.setState({hideHistory:"block"});}
        else{
            this.setState({hideHistory:"none"});
        }
    }
    show_audit_button(input){
        if(input===true){
            this.setState({hideAudit:"block"});}
        else{
            this.setState({hideAudit:"none"});
        }
    }

    show_systeminfo_button(input){
        if(input===true){
            this.setState({hideSystemInfo:"block"});}
        else{
            this.setState({hideSystemInfo:"none"});
        }
    }
    lock_all(bool){
        if(bool)
        this.setState({disabled:"disabled"});
        else
            this.setState({disabled:""});

    }

    hide_all(){
        this.setState({hideReturn:"none",hideLanguage:"none",hideTask:"none",hideParameter:"none",hideLocation:"none",hideHistory:"none",hideAudit:"none"});
    }
    handle_click_return(){
        console.log("click");
    }
    handle_click_language(){
        if(this.props.footcallbacklanguage){
            this.props.footcallbacklanguage();
        }
    }
    handle_click_task(){
        if(this.props.footcallbacktask){
            this.props.footcallbacktask();
        }
    }
    handle_click_parameter(){
        if(this.props.footcallbackparameter){
            this.props.footcallbackparameter();
        }
    }
    handle_click_location(){
        if(this.props.footcallbacklocation){
            this.props.footcallbacklocation();
        }
    }
    handle_click_system_info(){
        if(this.props.footcallbacksysteminfo){
            this.props.footcallbacksysteminfo();
            this.switch_button_icon();
            this.setState({systeminfo:"disabled"},this.release_system_info_button);
        }
    }
    release_system_info_button(){
        let self = this;
        setTimeout(function(){
            self.setState({systeminfo:""});
        },1000)
    }
    switch_button_icon(){
        if(this.state.icon == "fa fa-angle-double-left"){
            this.setState({icon:"fa fa-angle-double-right"});
        }else{
            this.setState({icon:"fa fa-angle-double-left"});
        }
    }
    disable(b_input){
        if(b_input){
            this.setState({disabled:"disabled"});
        }else{
            this.setState({disabled:""});
        }
    }

    render() {
        return (

            <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'100%',display:'table'}}>
                <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'50%',display:'table',float:"left"}}>

                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:"none"}} disabled={this.state.disabled} onClick={this.handle_click_return.bind(this)}>
                        <i className="fa fa-sign-out" style={{fontSize:25}}> </i>
                    </button>

                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideLanguage}} disabled={this.state.disabled} onClick={this.handle_click_language.bind(this)}>
                        <i className="fa fa-language" style={{fontSize:25}}> </i>
                    </button>

                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideTask}} disabled={this.state.disabled} onClick={this.handle_click_task.bind(this)}>
                        <i className="fa fa-tasks" style={{fontSize:25}}> </i>
                    </button>
                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideParameter}} disabled={this.state.disabled} onClick={this.handle_click_parameter.bind(this)}>
                        <i className="fa fa-sliders" style={{fontSize:25}}> </i>
                    </button>
                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideLocation}} disabled={this.state.disabled} onClick={this.handle_click_location.bind(this)}>
                        <i className="fa fa-crosshairs" style={{fontSize:25}}> </i>
                    </button>
                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideHistory}} disabled={this.state.disabled} onClick={this.handle_click_return.bind(this)}>
                        <i className="fa fa-history" style={{fontSize:25}}> </i>
                    </button>
                    <button  type="button" className="btn btn-warning btn-sm pull-left" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideAudit}} disabled={this.state.disabled} onClick={this.handle_click_return.bind(this)}>
                        <i className="fa fa-table" style={{fontSize:25}}> </i>
                    </button>
                    <a style={{position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle'}}>
                        < span className="headlabel" style={{fontSize:this.state.height*0.3,marginRight:this.state.height*0.3}}>&nbsp;</span>
                    </a>
                </div>

                <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'50%',display:'table',float:"left"}}>

                    <a style={{position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle'}}>
                        < span className="headlabel pull-right" style={{fontSize:this.state.height*0.3,marginRight:this.state.height*0.3}}>{this.state.language.content}</span>
                    </a>
                    <button  type="button" className="btn btn-warning btn-sm pull-right" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideSystemInfo}} disabled={this.state.systeminfo} onClick={this.handle_click_system_info.bind(this)}>
                        <i className={this.state.icon} style={{fontSize:25}}> </i>
                    </button>
                </div>
            </div>
        );
    }
}