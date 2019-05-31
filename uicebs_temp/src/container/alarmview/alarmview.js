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
import '../../../resource/css/font-awesome.min.css';



export default class alarmview extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            hide:"block",
            callback:null,
            margintop:20,
            language:{
                "alarm":"分辨率警告",
                "error":"系统错误"
            },
            iferror:false,
            alarm:"",
            error:""
        }
    }
    update_language(language){
        this.setState({language:language});
    }
    update_size(width,height){
        this.setState({height:height,width:width},this.calculate_margin);
    }
    calculate_margin(){
        let _modal = document.getElementById("kuangsmall");
        let module_height = _modal.offsetHeight;
        //if (_modal.innerHeight) module_height = _modal.innerHeight;
        //console.log("offsetHeight:"+_modal.offsetHeight+";innerHeight:"+_modal.clientHeight+",height"+_modal.style.height);
        if(((this.state.height - module_height)/2)>0){
            //console.log("Login marginTop:"+parseInt((this.state.height - module_height)/2)+",height:"+this.state.height+",module_height:"+module_height);
            this.setState({margintop:parseInt((this.state.height - module_height)/2)});
        }
    }
    update_error(error){
        this.setState({error:error,iferror:true});
    }
    update_alarm(alarm){
        this.setState({alarm:alarm});
    }
    hide(){
        this.setState({hide:"none"});
    }
    if_error(){
        return this.state.iferror;
    }
    show(){
        this.setState({hide:"block"});
    }
    render() {
        let center_panel;
        if(this.state.iferror){
            center_panel=
            <div className="panel panel-default" id="kuangsmall" >
                <div className="panel-heading">
                    <h3 className="panel-title" style={{color:"#000000",fontWeight:700}}>{this.state.language.error}</h3>
                </div>
                <div className="panel-body">
                    <h3 className="panel-title" style={{color:"#000000",fontWeight:300}}>{this.state.error}</h3>
                </div>
            </div>

        }else{
            center_panel=
                <div className="panel panel-default" id="kuangsmall" >
                    <div className="panel-heading">
                        <h3 className="panel-title" style={{color:"#000000",fontWeight:700}}>{this.state.language.alarm}</h3>
                    </div>
                    <div className="panel-body">
                        <h3 className="panel-title" style={{color:"#000000",fontWeight:300}}>{this.state.alarm}</h3>
                    </div>
                </div>
        }
        return (
            <div style={{position:"absolute",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:'100%',display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',backgroundImage: "url(./resource/image/zhihe.png)"
                ,backgroundRepeat:"no-repeat",backgroundSize:"100% 100%",MozBackgroundSize:"100% 100%",top:"0px",left:"0px",zIndex:"9999"}}>
                <div className="container">
                    <div className="leaderboard" style={{marginTop: this.state.margintop}}>
                        {center_panel}
                    </div>
                </div>
            </div>
        );
    }
}