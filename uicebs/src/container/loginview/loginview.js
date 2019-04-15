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
import './loginview.css';



export default class loginview extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            hide:"block",
            callback:null,
            margintop:20,
            language:{
                "title":"System Login",
                "username":"UserName",
                "password":"PassWord",
                "confirm":"Login"
            }
        }
        //this.keyboard_initialize();
    }
    update_language(language){
        this.setState({language:language});
    }
    update_size(width,height){
        this.setState({height:height,width:width},this.calculate_margin);

    }
    calculate_margin(){
        let _modal = document.getElementById("kuang");
        let module_height = _modal.offsetHeight;
        //if (_modal.innerHeight) module_height = _modal.innerHeight;
        //console.log("offsetHeight:"+_modal.offsetHeight+";innerHeight:"+_modal.clientHeight+",height"+_modal.style.height);
        if(((this.state.height - module_height)/2)>0){
            //console.log("Login marginTop:"+parseInt((this.state.height - module_height)/2)+",height:"+this.state.height+",module_height:"+module_height);
            this.setState({margintop:parseInt((this.state.height - module_height)/2)});
        }
    }
    update_callback(callback){
        this.setState({callback:callback});
    }
    hide(){
        this.setState({hide:"none"});
        $("#Username_Input").attr("disabled",true);
        $("#Password_Input").attr("disabled",true);
    }
    show(){
        this.setState({hide:"block"});
        $("#Username_Input").attr("disabled",false);
        $("#Password_Input").attr("disabled",false);
        $("#Password_Input").val("");

    }
    handle_login(){
        let username=document.getElementById("Username_Input").value;
        let password=document.getElementById("Password_Input").value;
        if (username === "") {
            document.getElementById("Username_Input").focus();
            return;
        }
        if (password === "") {
            document.getElementById("Password_Input").focus();
            return;
        }
        this.state.callback(username,password);
    }
    componentDidMount(){
    }
    componentDidUpdate(){
    }

    render() {
        return (
            <div className="loginbackground" style={{position:"relative",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:'100%',display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',backgroundImage: "url(./resource/image/zhihe.png)"
                ,backgroundRepeat:"no-repeat",backgroundSize:"100% 100%",MozBackgroundSize:"100% 100%"}}>
                <div className="container">
                    <div className="leaderboard" style={{marginTop: this.state.margintop}}>
                        <div className="panel panel-default" id="kuang" >
                            <div className="panel-heading">
                                <h3 className="panel-title" style={{color:"#000000",fontWeight:700}}>{this.state.language.title}</h3>
                            </div>
                            <div className="panel-body">
                                <div className="input-group">
                                    <span className="input-group-addon" id="Username" style={{minWidth: "100px",fontSize:"15px",color:"#000000",fontWeight:700}}>{this.state.language.username}</span>
                                    <input type="text" className="form-control login_user" placeholder={this.state.language.username} aria-describedby="basic-addon1" id="Username_Input"/>
                                </div>
                                <p></p>
                                <div className="input-group">
                                    <span className="input-group-addon" id="Password" style={{minWidth: "100px",fontSize:"15px",color:"#000000",fontWeight:700}}>{this.state.language.password}</span>
                                    <input type="password" className="form-control login_password" placeholder={this.state.language.password} aria-describedby="basic-addon1" id="Password_Input"/>
                                </div>
                                <p></p>
                                <button type="button" id="Login_Comfirm" data-loading-text="Loading..." className="btn btn-primary" autoComplete="off" style={{minWidth: "150px",color:"#ffffff",fontWeight:700,background:"#000000"}} onClick={this.handle_login.bind(this)} >
                                    {this.state.language.confirm}
                                </button>
                            </div>
                            <div className="clearfix"/>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}