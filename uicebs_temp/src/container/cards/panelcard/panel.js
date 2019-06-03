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
import './panel.css';



export default class panelcard extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            margin:75,
            status:"choice",
            hide:"none",
            showindex:"block",
            lock:"",
            animate:"animated fadeInRight",
            callback:null,
            margintop:20,
            key:"panelinfo",
            configure:{
                        "basic":{
                            "longitude":["1","2","3","4","5","6"],
                            "latitude":[],
                            "name":"2x3",
                            "batch":"",
                            "date":"",
                            "analysis": false,
                            "video": false,
                            "parameter":{
                            "smallsize":200,
                                "smallmiddle":500,
                                "middlelarge":2000,
                                "largesize":5000,
                                "extra1":0,
                                "extra2":0,
                                "extra3":0,
                                "extra4":0
                            },
                            "owner":"",
                            "tupid":"",
                            "extra":[{"title":"","value":""}]
                        },
                        "picture":[],
                        "pictureclass":{
                            "series":"",
                            "shooting":"false",
                            "videoing":"false",
                            "analysising":"false",
                            "shoot":[],
                            "video":"",
                            "analysis":{
                                "resultPic":"",
                                    "result":[{"title":"","value":""}]
                            }
                    }

                },
            language:{
                "panelinfo":"托盘状态",
                "consoletitle":"实时日志",
                "batch":"批次",
                "date":"日期",
                "owner":"操作人",
                "tupid":"tupid"
            }
        }
    }
    update_language(language){
        this.setState({language:language});
    }
    update_size(width,height,margin){
        this.setState({height:height,width:width,margin:margin});
    }
    update_configure(configure){
        this.setState({configure:configure});
    }
    get_configure(){
        return this.state.configure;
    }
    change_status(mode){
        if(mode === "running"){
            this.setState({status:"running"});
            this.show_index(false);
            this.disable_button(true);
        }else if(mode === "view"){
            this.setState({status:"view"});
            this.show_index(false);
            this.disable_button(false);
        }else{
            this.setState({status:"choice"});
            this.show_index(true);
            this.disable_button(false);
        }
    }
    show_index(bool){
        if(bool){
            this.setState({showindex:"block"});
        }else{
            this.setState({showindex:"none"});
        }
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
    disable_button(bool){
        if(bool){
            this.setState({lock:"disabled"});
        }else{
            this.setState({lock:""});
        }
    }
    if_selected(id){
        if(this.state.configure == null) return false;
        for(let i=0;i<this.state.configure.picture.length;i++){
            if(id === this.state.configure.picture[i].series){
                return true;
            }
        }
        return false;
    }
    get_result(id){
        if(this.state.configure == null) return null;
        for(let i=0;i<this.state.configure.picture.length;i++){
            if(id === this.state.configure.picture[i].series){
                return this.state.configure.picture[i];
            }
        }
        return null;
    }
    if_button_selected(index){
        if(this.state.configure.basic.latitude.length ===0){
            if(this.if_selected(index)) return "holebutton-selected";
            else return "holebutton";
        }

        if(index === "all"){
            if(this.state.configure.basic.latitude.length ===0){
               if(this.state.configure.picture.length==6) return "indexbutton-selected";
               else return "indexbutton";
            }else{
                if(this.state.configure.picture.length==this.state.configure.basic.latitude.length*this.state.configure.basic.longitude.length) return "indexbutton-selected";
                else return "indexbutton";
            }
        }else{
            if(this.state.configure.basic.latitude.indexOf(index)>=0){
                for(let i=0;i<this.state.configure.basic.longitude.length;i++){
                    if(!this.if_selected(index+this.state.configure.basic.longitude[i])) return "indexbutton";
                }
                return "indexbutton-selected";
            }else if(this.state.configure.basic.longitude.indexOf(index)>=0){
                for(let i=0;i<this.state.configure.basic.latitude.length;i++){
                    if(!this.if_selected(this.state.configure.basic.latitude[i]+index)) return "indexbutton";
                }
                return "indexbutton-selected";
            }else{
                if(this.if_selected(index)) return "holebutton-selected";
                else return "holebutton";
            }
        }
    }
    get_run_status(id){
        if(this.state.configure == null) return null;
        for(let i=0;i<this.state.configure.picture.length;i++){
            if(id === this.state.configure.picture[i].series){
                return this.state.configure.picture[i];
            }
        }
        return null;
    }
    if_show_run(){
        if(this.state.status == "choice") return false;
        return true;
    }

    handle_click(event){
        let key = event.target.getAttribute("data-key-series");
        if(this.state.status === "choice"){
            if(this.state.configure.basic.latitude.length ===0){
                if(this.if_selected(key)){
                    this.remove_selected(key);
                }else{
                    this.add_selected(key);
                }
                return;
            }
            //console.log("button clicked:"+key);
            if(key === "all"){
                if(this.if_button_selected("all") ==="indexbutton-selected"){
                    //console.log("should remove all");
                    this.remove_all();
                }else{

                    //console.log("should select all");
                    this.select_all();
                }
            }else{
                if(this.state.configure.basic.latitude.indexOf(key)>=0){
                    if(this.if_button_selected(key) ==="indexbutton-selected"){

                        //console.log("should remove index:"+key);
                        this.remove_index_selected(key);
                    }else{

                        //console.log("should select index:"+key);
                        this.add_index_selected(key);
                    }
                }else if(this.state.configure.basic.longitude.indexOf(key)>=0){
                    if(this.if_button_selected(key) ==="indexbutton-selected"){

                        //console.log("should remove index:"+key);
                        this.remove_index_selected(key);
                    }else{
                        //console.log("should select index:"+key);
                        this.add_index_selected(key);
                    }
                }else{
                    if(this.if_selected(key)){
                        this.remove_selected(key);
                    }else{
                        this.add_selected(key);
                    }
                }
            }
        }else{
            console.log("view clicked:"+key);
            let result = this.get_result(key);
            if(result!== null){

                this.props.showresult(result);
            }
        }

    }
    //TODO:Should check if we really need deep copy here,specially we need to face batch modification
    add_selected(id){
        if(this.if_selected(id)) return;
        else{
            let temp = jsondeepCopy(this.state.configure);
            let newchoice = jsondeepCopy(temp.pictureclass);
            newchoice.series = id;
            newchoice.shoot = [];
            temp.picture.push(newchoice);
            this.setState({configure:temp});
        }
    }
    remove_selected(id){
        if(!this.if_selected(id)) return;
        else{
            let temp = jsondeepCopy(this.state.configure);
            for(let i=0;i<temp.picture.length;i++){
                if(id === temp.picture[i].series){
                    temp.picture.splice(i,1);
                    break;
                }
            }
            this.setState({configure:temp});
        }
    }
    build_series_list(index){
        let ret = [];
        if(this.state.configure.basic.latitude.length ===0){
            if(index == "all"){
                ret = this.state.configure.basic.longitude;
            }else{
                ret.push(index);
            }
            return ret;
        }
        if(index =="all"){
                for(let i=0;i<this.state.configure.basic.latitude.length;i++){
                    for(let j=0;j<this.state.configure.basic.longitude.length;j++){
                        ret.push(this.state.configure.basic.latitude[i]+this.state.configure.basic.longitude[j]);
                    }
                }

        }else{
            if(this.state.configure.basic.latitude.indexOf(index)>=0){
                for(let i=0;i<this.state.configure.basic.longitude.length;i++){
                    ret.push(index+this.state.configure.basic.longitude[i]);
                }
            }else if(this.state.configure.basic.longitude.indexOf(index)>=0){
                for(let i=0;i<this.state.configure.basic.latitude.length;i++){
                    ret.push(this.state.configure.basic.latitude[i]+index);
                }
            }else{
                ret.push(index);
            }
        }
        return ret;
    }
    select_all(){
        let temp = jsondeepCopy(this.state.configure);
        temp.picture=[];
        let all_list = this.build_series_list("all");
        for(let i=0;i<all_list.length;i++){
            let newchoice = jsondeepCopy(temp.pictureclass);
            newchoice.series = all_list[i];
            newchoice.shoot = [];
            temp.picture.push(newchoice);
        }
        this.setState({configure:temp});
    }
    remove_all(){
        let temp = jsondeepCopy(this.state.configure);
        temp.picture=[];
        this.setState({configure:temp});
    }
    add_index_selected(index){
        let temp = jsondeepCopy(this.state.configure);
        let all_list = this.build_series_list(index);
        for(let i=0;i<all_list.length;i++){
            if(!this.if_selected(all_list[i])){
                let newchoice = jsondeepCopy(temp.pictureclass);
                newchoice.series = all_list[i];
                temp.picture.push(newchoice);
            }
        }
        this.setState({configure:temp});
    }
    remove_index_selected(index){
        let temp = jsondeepCopy(this.state.configure);
        let all_list = this.build_series_list(index);
        //console.log(all_list);
        for(let i=0;i<all_list.length;i++){
            for(let j=0;j<temp.picture.length;j++){
                if(temp.picture[j].series === all_list[i]){
                    temp.picture.splice(j,1);
                    break;
                }
            }
        }
        this.setState({configure:temp});
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
    clearruninfo(){
        let temp = jsondeepCopy(this.state.configure);
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
        this.setState({configure:temp});
        this.change_status("choice");
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
        let line= 0;
        let row=0;
        let size = "";
        let buttons = [];
        let margin = "5px";
        let font = "15px";
        let weight ="700"
        if(this.state.configure.basic.latitude.length ===0){
            //special for 2x3 layout;
            line = 2;
            row=3;
        }else{
            line = this.state.configure.basic.latitude.length+1;
            row = this.state.configure.basic.longitude.length+1;
        }
        if(row>10) {
            margin = "1px";
            font="50%";
            weight="100"
        }
        size = parseInt(this.state.width*0.8/(row+1));
        if(size*(line+1)>(this.state.height*0.9)) size = parseInt(this.state.height*0.9/(line+1));
        for(let i=0;i<line;i++){
            let buttonline=[];
            for(let j=0;j<row;j++){
                let button;
                if(line === 2 & row ===3){
                    //special: no line and row all choice
                    if(this.if_show_run()){
                        let picclass = this.get_run_status(this.state.configure.basic.longitude[i*3+j])

                        let classstring = "btn  btn-sm pull-left ";
                        let iconclass = "";
                        if(picclass === null){
                            classstring = classstring+"holebutton"
                        }else{
                            if(picclass.shooting === "true"||picclass.videoing === "true"||picclass.analysising === "true" )    {
                                if(picclass.analysising === "true"){
                                    classstring = classstring+"holebutton-selected "+"blingbling-LGREEN green-button";
                                    iconclass = "fa fa-clipboard"
                                }else if(picclass.videoing === "true"){
                                    classstring = classstring+"holebutton-selected "+"blingbling-ORANGE orange-button";
                                    iconclass = "fa fa-video-camera"
                                }else{
                                    classstring = classstring+"holebutton-selected "+"blingbling-LBLUE blue-button";
                                    iconclass = "fa fa-camera-retro"
                                }
                            }else if(picclass.shooting === "done"||picclass.videoing === "done"||picclass.analysising === "done" ){
                                if(picclass.analysising === "done"){
                                    classstring = classstring+"holebutton-selected "+"green-button";
                                    iconclass = "fa fa-clipboard"
                                }else if(picclass.videoing === "done"){
                                    classstring = classstring+"holebutton-selected "+"orange-button";
                                    iconclass = "fa fa-video-camera"
                                }else{
                                    classstring = classstring+"holebutton-selected "+"blue-button";
                                    iconclass = "fa fa-camera-retro"
                                }
                            }else{
                                classstring = classstring+"holebutton-selected "
                            }
                        }

                        button =
                            <button  type="button" className={classstring}
                                     style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px"}}
                                     data-key-series =  {this.state.configure.basic.longitude[i*3+j]}
                                     onClick={this.handle_click.bind(this)}
                                     disabled={this.state.lock}
                                     key =  {this.state.configure.basic.longitude[i*3+j]}>
                                <i data-key-series =  {this.state.configure.basic.longitude[i*3+j]}
                                   className={iconclass}
                                   style={{fontSize:font}}>
                                    {this.state.configure.basic.longitude[i*3+j]}</i>
                            </button>
                    }else{

                        button =
                            <button  type="button" className={"btn  btn-sm pull-left "+this.if_button_selected(this.state.configure.basic.longitude[i*3+j])}
                                     style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px"}}
                                     data-key-series = {this.state.configure.basic.longitude[i*3+j]}
                                     onClick={this.handle_click.bind(this)}
                                     disabled={this.state.lock}
                                     key = {this.state.configure.basic.longitude[i*3+j]}>
                                <i data-key-series = {this.state.configure.basic.longitude[i*3+j]}
                                   style={{fontSize:font}}>
                                    {this.state.configure.basic.longitude[i*3+j]}</i>
                            </button>
                    }
                    /*
                    button = <button  type="button" className={"btn  btn-sm pull-left "+this.if_button_selected(this.state.configure.basic.longitude[i*3+j])}
                                      style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px"}}
                             data-key-series={this.state.configure.basic.longitude[i*3+j]}
                                      onClick={this.handle_click.bind(this)}

                    key = {this.state.configure.basic.longitude[i*3+j]}>
                        <i data-key-series={this.state.configure.basic.longitude[i*3+j]}
                           style={{fontSize:font}}>
                            {this.state.configure.basic.longitude[i*3+j]}</i>
                    </button>*/
                }else{
                    if(i===0){
                        if(j===0){
                            button =
                                <button  type="button" className={"btn  btn-sm pull-left "+this.if_button_selected("all")}
                                         style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px",display:this.state.showindex}}
                                         data-key-series={"all"}
                                         onClick={this.handle_click.bind(this)} key={"all"}>
                                    <i data-key-series={"all"}
                                       style={{fontSize:font}}>
                                        {"all"}</i>
                                </button>
                        }else{
                            button =
                                <button  type="button" className={"btn  btn-sm pull-left "+this.if_button_selected(this.state.configure.basic.longitude[j-1])}
                                         style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px",display:this.state.showindex}}
                                         data-key-series={this.state.configure.basic.longitude[j-1]}
                                         onClick={this.handle_click.bind(this)} key = {this.state.configure.basic.longitude[j-1]}>
                                    <i data-key-series={this.state.configure.basic.longitude[j-1]}
                                       style={{fontSize:font}}>
                                        {this.state.configure.basic.longitude[j-1]}</i>
                                </button>
                        }
                    }else{
                        if(j===0){
                            button =
                                <button  type="button" className={"btn  btn-sm pull-left "+this.if_button_selected(this.state.configure.basic.latitude[i-1])}
                                         style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px",display:this.state.showindex}}
                                         data-key-series = {this.state.configure.basic.latitude[i-1]}
                                         onClick={this.handle_click.bind(this)}
                                         key = {this.state.configure.basic.latitude[i-1]}>
                                    <i data-key-series = {this.state.configure.basic.latitude[i-1]}
                                       style={{fontSize:font}}>
                                        {this.state.configure.basic.latitude[i-1]}</i>
                                </button>
                        }else{
                            if(this.if_show_run()){
                                let picclass = this.get_run_status(this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1])

                                let classstring = "btn  btn-sm pull-left ";
                                let iconclass = "";
                                if(picclass === null){
                                    classstring = classstring+"holebutton"
                                }else{
                                    if(picclass.shooting === "true"||picclass.videoing === "true"||picclass.analysising === "true" )    {
                                        if(picclass.analysising === "true"){
                                            classstring = classstring+"holebutton-selected "+"blingbling-LGREEN green-button";
                                            iconclass = "fa fa-clipboard"
                                        }else if(picclass.videoing === "true"){
                                            classstring = classstring+"holebutton-selected "+"blingbling-ORANGE orange-button";
                                            iconclass = "fa fa-video-camera"
                                        }else{
                                            classstring = classstring+"holebutton-selected "+"blingbling-LBLUE blue-button";
                                            iconclass = "fa fa-camera-retro"
                                        }
                                    }else if(picclass.shooting === "done"||picclass.videoing === "done"||picclass.analysising === "done" ){
                                        if(picclass.analysising === "done"){
                                            classstring = classstring+"holebutton-selected "+"green-button";
                                            iconclass = "fa fa-clipboard"
                                        }else if(picclass.videoing === "done"){
                                            classstring = classstring+"holebutton-selected "+"orange-button";
                                            iconclass = "fa fa-video-camera"
                                        }else{
                                            classstring = classstring+"holebutton-selected "+"blue-button";
                                            iconclass = "fa fa-camera-retro"
                                        }
                                    }else{
                                        classstring = classstring+"holebutton-selected "
                                    }
                                }

                                button =
                                    <button  type="button" className={classstring}
                                             style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px"}}
                                             data-key-series = {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}
                                             onClick={this.handle_click.bind(this)}
                                             disabled={this.state.lock}
                                             key = {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}>
                                        <i data-key-series = {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}
                                           className={iconclass}
                                           style={{fontSize:font}}>
                                            {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}</i>
                                    </button>
                            }else{

                                button =
                                    <button  type="button" className={"btn  btn-sm pull-left "+this.if_button_selected(this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1])}
                                             style={{padding:"0px",marginLeft:margin,marginTop:margin,height:size,width:size,borderRadius: size/2+"px"}}
                                             data-key-series = {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}
                                             onClick={this.handle_click.bind(this)}
                                             disabled={this.state.lock}
                                             key = {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}>
                                        <i data-key-series = {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}
                                           style={{fontSize:font}}>
                                            {this.state.configure.basic.latitude[i-1]+this.state.configure.basic.longitude[j-1]}</i>
                                    </button>
                            }
                        }

                    }
                }
                buttonline.push(button);
            }
            buttons.push(
                <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12"  key={"line"+i}>{buttonline}</div>
            )
        }


        let panel =
            <div style={{width:"98%"}}>
                {buttons}
            </div>
        return (
            <div className={this.state.animate} style={{position:"absolute",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:this.state.width,top:0,right:0,display:this.state.hide,overflow:'scroll',overflowX:'hidden',overflowY:'hidden',zIndex:"99"}}>
                <div className="col-xs-12 col-md-12 col-sm-12 col-lg-12" key="status-top">
                    <div className="tile-stats"  style={{marginTop:"15px"}}>
                        <div className="count" style={{fontSize:24}}>{this.state.language.panelinfo}</div>

                            {panel}

                    </div>
                </div>
            </div>
        );
    }
}