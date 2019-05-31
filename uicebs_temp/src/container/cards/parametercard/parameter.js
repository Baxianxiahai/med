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
import { jsondeepCopy } from '../../../util/util.js';
import './parameter.css';



export default class parametercard extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            footheight:100,
            margin:75,
            hide:"none",
            animate:"animated fadeInLeft",
            callback:null,
            margintop:20,
            content:[],
            configure:null,
            key:"sys_conf_key",
            key2:"sys_conf_input",
            callbackSave:null,
            language:{
                "parameterinfo":"系统参数",
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
    update_callback(callback){
        this.setState({callback:callback});
    }
    update_config(configure){
        this.setState({configure:configure});
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

    handleChange(e){
        let change_value = e.target.value;
        let group_id= parseInt(e.target.getAttribute('data-group'));
        let parameter_id= parseInt(e.target.getAttribute('data-parameter'));

        let new_state = jsondeepCopy(this.state.configure);
        new_state.parameter.groups[group_id].list[parameter_id].value=change_value;
        this.setState({configure:new_state});
    }
    handleBlur(){

    }
    handleSave(){

    }
    handleChangecheck(){

    }
    getUpdatedValue(){
        let config = this.state.configure;
        for(let i=0;i<config.parameter.groups.length;i++){
            for(let j=0;j<config.parameter.groups[i].list.length;j++){
                if(config.parameter.groups[i].list[j].type === "int"){
                    config.parameter.groups[i].list[j].value=$("#"+this.state.key2+"G"+i+"P"+j+config.parameter.groups[i].list[j].type).val();
                }
                if(config.parameter.groups[i].list[j].type === "float"){
                    config.parameter.groups[i].list[j].value=$("#"+this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type).val();
                }
                if(this.state.configure.parameter.groups[i].list[j].type === "string"){
                    this.state.configure.parameter.groups[i].list[j].value=$("#"+this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type).val();
                }
                if(this.state.configure.parameter.groups[i].list[j].type === "choice"){
                    this.state.configure.parameter.groups[i].list[j].value=$("#"+this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type).get(0).selectedIndex+"";//val();
                }
                if(this.state.configure.parameter.groups[i].list[j].type === "checkbox"){
                    this.state.configure.parameter.groups[i].list[j].value=$("#"+this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type).is(":checked");
                }
            }
        }
        return config;
    }
    update_callback_save(callback){
        this.setState({callbackSave:callback})
    }

    handle_click_save(){
        this.state.callbackSave();

    }
    switchery_initialize(){
        $(".sys-conf-checkbox-label").each(function(){
            $(this).find("span").each(function(){
                $(this).remove();
            });
        });
        /*
         let switchery_list = $("#preemption_tab").find("span").each(function(){
         $(this).remove();
         });*/
        if(this.state.configure!==null){

            for(let i=0;i<this.state.configure.parameter.groups.length;i++){
                for(let j=0;j<this.state.configure.parameter.groups[i].list.length;j++){
                    if(this.state.configure.parameter.groups[i].list[j].type === "checkbox"){
                        $("#"+this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type).prop("checked",this.state.configure.parameter.groups[i].list[j].value);
                    }
                }

            }
        }

        if ($(".sys_conf_checkbox")[0]) {
            var elems = Array.prototype.slice.call(document.querySelectorAll('.sys_conf_checkbox'));
            //console.log("switchery list lenght:"+elems.length);
            elems.forEach(function (html) {
                var switchery = new Switchery(html, {
                    color: '#26B99A'
                });
            });
        }
    }
    componentDidMount(){
        //this.keyboard_initialize();
    }
    componentDidUpdate(){
        this.switchery_initialize();
    }
    render() {
        let groups1 = [];
        let grougs1size=0;
        let groups2 = [];
        let groups2size=0;
        if(this.state.configure!= null){

            for(let i=0;i<this.state.configure.parameter.groups.length;i++){
                let param = [];
                for(let j=0;j<this.state.configure.parameter.groups[i].list.length;j++){
                    if(this.state.configure.parameter.groups[i].list[j].type === "int"){
                        let contentline = "["+this.state.configure.parameter.groups[i].list[j].min+"->"+this.state.configure.parameter.groups[i].list[j].max+"]:"+this.state.configure.parameter.groups[i].list[j].note;
                        let className="form-control "+"sys_conf_input_"+this.state.configure.parameter.groups[i].list[j].type;
                        param.push(
                            <div className="count" style={{fontSize:20,marginTop:15,verticalAlign:'bottom',width:"90%"}} key={this.state.key+i+"p"+j+"l"}>
                                <div className="input-group">
                                    <span className="input-group-addon"  style={{minWidth: "100px",fontSize:"12px"}}>{this.state.configure.parameter.groups[i].list[j].paraname+":"}</span>
                                    <input type="text" className={className} placeholder="CONFIG Value" aria-describedby="basic-addon1"
                                           key={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} id={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} data-group={i} data-parameter={j}
                                           value={this.state.configure.parameter.groups[i].list[j].value} onChange={this.handleChange.bind(this)} onBlur={this.handleBlur.bind(this)}
                                           data-min={this.state.configure.parameter.groups[i].list[j].min} data-max={this.state.configure.parameter.groups[i].list[j].max}/>
                                </div>
                                <h3 style={{fontSize:15,marginRight:5,color:"#333"}}  key={this.state.key2+i+"p"+j+"2"}>{contentline}</h3>
                            </div>);
                    }
                    if(this.state.configure.parameter.groups[i].list[j].type === "float"){
                        let contentline = "["+this.state.configure.parameter.groups[i].list[j].min+"->"+this.state.configure.parameter.groups[i].list[j].max+"]:"+this.state.configure.parameter.groups[i].list[j].note;
                        let className="form-control "+"sys_conf_input_"+this.state.configure.parameter.groups[i].list[j].type;
                        param.push(
                            <div className="count" style={{fontSize:20,marginTop:15,verticalAlign:'bottom',width:"90%"}} key={this.state.key+i+"p"+j+"l"}>
                                <div className="input-group">
                                    <span className="input-group-addon" style={{minWidth: "100px",fontSize:"12px"}}>{this.state.configure.parameter.groups[i].list[j].paraname+":"}</span>
                                    <input type="text" className={className} placeholder="CONFIG Value" aria-describedby="basic-addon1"
                                           key={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} id={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} data-group={i} data-parameter={j}
                                           value={this.state.configure.parameter.groups[i].list[j].value} onChange={this.handleChange.bind(this)} onBlur={this.handleBlur.bind(this)}
                                           data-min={this.state.configure.parameter.groups[i].list[j].min} data-max={this.state.configure.parameter.groups[i].list[j].max}/>
                                </div>
                                <h3 style={{fontSize:15,marginRight:5,color:"#333"}}  key={this.state.key2+i+"p"+j+"2"}>{contentline}</h3>
                            </div>);
                    }
                    if(this.state.configure.parameter.groups[i].list[j].type === "string"){
                        //let contentline = "Max length:["+this.state.configure.parameter.groups[i].list[j].max+"];Note:"+this.state.configure.parameter.groups[i].list[j].note;
                        let contentline = this.state.configure.parameter.groups[i].list[j].note;
                        let className="form-control "+"sys_conf_input_"+this.state.configure.parameter.groups[i].list[j].type;
                        param.push(
                            <div className="count" style={{fontSize:20,marginTop:15,verticalAlign:'bottom',width:"90%"}} key={this.state.key+i+"p"+j+"l"}>
                                <div className="input-group">
                                    <span className="input-group-addon"  style={{minWidth: "100px",fontSize:"12px"}}>{this.state.configure.parameter.groups[i].list[j].paraname+":"}</span>
                                    <input type="text" className={className} placeholder="CONFIG Value" aria-describedby="basic-addon1"
                                           key={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} id={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} data-group={i} data-parameter={j}
                                           value={this.state.configure.parameter.groups[i].list[j].value} onChange={this.handleChange.bind(this)} onBlur={this.handleBlur.bind(this)}
                                           data-min={this.state.configure.parameter.groups[i].list[j].min} data-max={this.state.configure.parameter.groups[i].list[j].max}/>
                                </div>
                                <h3 style={{fontSize:15,marginRight:5,color:"#333"}}  key={this.state.key2+i+"p"+j+"2"}>{contentline}</h3>
                            </div>);
                    }
                    if(this.state.configure.parameter.groups[i].list[j].type === "choice"){
                        let contentline = this.state.configure.parameter.groups[i].list[j].note;
                        let className="form-control "+"sys_conf_choice";
                        let choice_items = [];
                        //this.state.configure.parameter.groups[i].list[j].value = this.state.configure.parameter.groups[i].list[j].items[parseInt(this.state.configure.parameter.groups[i].list[j].value)];
                        for(let k=0;k<this.state.configure.parameter.groups[i].list[j].items.length;k++){
                            /*if(k === parseInt(this.state.configure.parameter.groups[i].list[j].value))
                             choice_items.push(<option value={this.state.configure.parameter.groups[i].list[j].items[k]} key={"choice_item_"+i+"_"+j+"_"+k} selected="selected">{this.state.configure.parameter.groups[i].list[j].items[k]}</option>);
                             else*/
                            choice_items.push(<option value={k+""} key={"choice_item_"+i+"_"+j+"_"+k}>{this.state.configure.parameter.groups[i].list[j].items[k]}</option>);


                        }
                        param.push(
                            <div className="count" style={{fontSize:20,marginTop:15,verticalAlign:'bottom',width:"90%"}} key={this.state.key+i+"p"+j+"l"}>
                                <div className="input-group">
                                    <span className="input-group-addon"  style={{minWidth: "100px",fontSize:"12px"}}>{this.state.configure.parameter.groups[i].list[j].paraname+":"}</span>
                                    <select className={className} placeholder="CONFIG Value" aria-describedby="basic-addon1"
                                            key={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} id={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} data-group={i} data-parameter={j}
                                            onChange={this.handleChange.bind(this)} onBlur={this.handleBlur.bind(this)}
                                            value={this.state.configure.parameter.groups[i].list[j].value} >{choice_items}</select>
                                </div>
                                <h3 style={{fontSize:15,marginRight:5,color:"#333"}}  key={this.state.key2+i+"p"+j+"2"}>{contentline}</h3>
                            </div>);



                    }
                    if(this.state.configure.parameter.groups[i].list[j].type === "checkbox"){
                        if(this.state.configure.parameter.groups[i].list[j].value){

                            let temp =<div className="count" style={{fontSize:20,marginTop:15,verticalAlign:'bottom',width:"90%"}} key={this.state.key+i+"p"+j+"l"}>
                                <div>
                                    <label className="sys-conf-checkbox-label" style={{fontSize: "16px",color:"#555"}}>
                                        {this.state.configure.parameter.groups[i].list[j].paraname+":"}&nbsp;&nbsp;&nbsp;&nbsp;
                                        <input type="checkbox" id={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} className="js-switch sys_conf_checkbox" defaultChecked="checked" onChange={this.handleChangecheck.bind(this)} data-switchery="true" value="on"/>
                                    </label>
                                </div></div>;
                            param.push(temp);
                        }else{
                            let temp = <div className="count" style={{fontSize:20,marginTop:15,verticalAlign:'bottom',width:"90%"}} key={this.state.key+i+"p"+j+"l"}>
                                <div>
                                    <label className="sys-conf-checkbox-label" style={{fontSize: "16px",color:"#555"}}>
                                        {this.state.configure.parameter.groups[i].list[j].paraname+":"}&nbsp;&nbsp;&nbsp;&nbsp;
                                        <input type="checkbox" id={this.state.key2+"G"+i+"P"+j+this.state.configure.parameter.groups[i].list[j].type} className="js-switch sys_conf_checkbox" onChange={this.handleChangecheck.bind(this)} data-switchery="true" value="on"/>
                                    </label>
                                </div></div>;
                            param.push(temp);
                        }
                    }
                }
                if(grougs1size<=groups2size){
                    groups1.push(
                        <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key={this.state.key+i+"p"}>
                            <div className="tile-stats" key={"configure_group_"+this.state.configure.parameter.groups[i].groupname} style={{marginTop:"15px"}}>
                                <div key="statuspanel" className="count" style={{fontSize:24}}>{this.state.configure.parameter.groups[i].groupname}</div>
                                {param}
                            </div>
                        </div>
                    );
                    grougs1size = grougs1size+this.state.configure.parameter.groups[i].list.length;
                }else{
                    groups2.push(
                        <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key={this.state.key+i+"p"}>
                            <div className="tile-stats" key={"configure_group_"+this.state.configure.parameter.groups[i].groupname} style={{marginTop:"15px"}}>
                                <div key="statuspanel" className="count" style={{fontSize:24}}>{this.state.configure.parameter.groups[i].groupname}</div>
                                {param}
                            </div>
                        </div>
                    );
                    groups2size = groups2size+this.state.configure.parameter.groups[i].list.length;
                }


            }

        }
        return (
            <div className={this.state.animate} style={{position:"absolute",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:this.state.width,top:0,left:0,display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',zIndex:"99"}}>
                <div style={{float: "left",position:"relative",width:((this.state.footheight-10)*1.6+10),height:this.state.height,borderRight:"solid 2px #dddddd"}}>
                    <button  type="button" className="btn btn-warning btn-sm pull-right" style={{marginLeft:"5px",marginTop:"5px",height:(this.state.footheight-10)*1.6,width:(this.state.footheight-10)*1.6,display:this.state.hideSave}} disabled={this.state.disabled} onClick={this.handle_click_save.bind(this)}>
                        <i className="fa fa-save" style={{fontSize:25}}> </i>
                    </button>
                </div>
                <div id='sysconfview'   style={{float: "left",position:"relative",width:this.state.width-((this.state.footheight-10)*1.6+10),height:this.state.height,overflowY:"auto",overflowX:"hidden"}}>
                    <div className="container" >
                        <div className="col-xs-6 col-md-6 col-sm-6 col-lg-6">
                            {groups1}
                        </div>
                        <div className="col-xs-6 col-md-6 col-sm-6 col-lg-6">
                            {groups2}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}