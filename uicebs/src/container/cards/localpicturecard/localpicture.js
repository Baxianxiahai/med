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



export default class localpicturecard extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            margin:75,
            hide:"none",
            animate:"animated fadeInRight",
            callback:null,
            margintop:20,
            content:[],
            key:"pictureinfo",
            language:{
                "pictureinfo":"本地图片",
                "consoletitle":"实时日志"
            }
        }
    }
    update_language(language){
        this.setState({language:language});
    }
    update_size(width,height,margin){
        this.setState({height:height,width:width,margin:margin});
    }
    update_content(content){
        this.setState({content:content});
    }
    hide(){
        if(this.state.hide === "none") return;
        else{
            this.setState({animate:"animated fadeOutRight"});
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
            this.setState({hide:"block",animate:"animated fadeInRight"});
        }
    }
    switch_system_info(){
        if(this.state.hide == "none"){
            this.setState({hide:"block",animate:"animated fadeInRight"});
        }else{
            this.setState({animate:"animated fadeOutRight"});
            let self = this;
            setTimeout(function(){
                self.setState({hide:"none"});
            },800);
        }
    }
    render() {

        return (
            <div className={this.state.animate} style={{position:"absolute",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:this.state.width,top:0,right:0,display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',zIndex:"99"}}>
                <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key="status-top">
                    <div className="tile-stats"  style={{marginTop:"15px"}}>
                        <div className="count" style={{fontSize:24}}>{this.state.language.pictureinfo}</div>

                    </div>
                </div>
            </div>
        );
    }
}