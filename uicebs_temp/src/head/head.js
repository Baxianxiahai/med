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
import './head.css';

export default class head extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:50,
            username:"",
            "loginfo":"xxxxxxxxx",
            "clock":"xx-xx-xx xx:xx",
            hideUser:"none",
            hide:"table",
            language:{
                "icon":"",
                "nologin":"no login",
                "title":"智能模式生物检测平台",
                "greet":"Hello"
            }
        }
    }
    update_language(language){
        this.setState({language:language,username:language.nologin});
    }
    update_size(height){
        this.setState({height:height})
    }
    update_username(username){
        this.setState({username:username});
        this.show_button();
    }
    show_user_button(buser){
        if(buser){
            this.show_button();
        }else{
            this.hide_button();
        }
    }
    hide_button(){
        this.setState({hideUser:"none"});
    }
    show_button(){
        this.setState({hideUser:"block"});
    }

    update_clock(clock){
        this.setState({clock:clock})
    }
    handle_click_user(){
        if(this.props.headcallbackuser){
            this.props.headcallbackuser();
        }
    }
    hide(){
        this.setState({hide:"none"});
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
    render() {
        let temp = this.state.language.greet+this.state.username;
        if(this.state.username === ""){
            temp = this.state.language.greet;
        }
        return (
            <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'100%',display:this.state.hide}}>
                <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'33%',display:'table',float:"left"}}>
                    <a style={{position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle',width:this.state.height}}><i style={{marginLeft:this.state.height*0.3,fontSize:this.state.height*0.5,color:"#62b900"}}><img src="./resource/image/logo.png"  style={{height:this.state.height*0.8,width:this.state.height*0.8,zIndex: -1}}></img></i>
                    </a>
                    <a style={{position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle'}}><span className="headlabel" style={{fontSize:this.state.height*0.3,marginLeft:20}}>{this.state.language.title}</span></a>
                </div>
                <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'33%',display:'table',float:"left"}}>
                    <a style={{position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle',textAlign:"center"}}>
                        < span className="headlabel" style={{fontSize:this.state.height*0.3,marginRight:this.state.height*0.3}}>{this.state.loginfo}</span>
                    </a>
                </div>
                <div style={{position:"relative",background:"#eeeeee",height:this.state.height,width:'33%',display:'table',float:"left"}}>

                    <a style={{position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle'}}>< span className="headlabel pull-right" style={{fontSize:this.state.height*0.2,marginRight:this.state.height*0.3}}>{temp}</span></a>

                    <a style={{marginLeft:'10px',position:"relative",height:this.state.height,display:'table-cell',verticalAlign:'middle'}}>< span className="headlabel pull-right" style={{fontSize:this.state.height*0.2,marginRight:this.state.height*0.3}}>{this.state.clock}</span></a>
                    <button  type="button" className="btn btn-warning btn-sm pull-right" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.height-10),width:(this.state.height-10)*1.6,display:this.state.hideUser}} disabled={this.state.disabled} onClick={this.handle_click_user.bind(this)}>
                        <i className="fa fa-user-o" style={{fontSize:25}}> </i>
                    </button>
                </div>
            </div>
        );
    }
}