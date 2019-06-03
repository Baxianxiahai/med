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
import Languagebrick from './languagebrick/languagebrick';
//import Rodal    from './rodal/rodal';
import '../../../resource/css/font-awesome.min.css';
import './languageview.css';



export default class languageview extends Component {
    constructor(props) {
        super(props);
        this.state={
            height:700,
            width:600,
            buttonlist:[],
            baselist:[],
            hide:"block",
            bricksize:100,
            marginsize:5,
            key:"brick",
            callback:null,
            newchoicecallback:null,
            moduleshow:false,
            moduleanimation:'door'
        }
    }
    update_language(language){
        //this.setState({language:language});
    }
    update_size(width,height){
        this.calculatesize(width);
        this.setState({height:height,width:width});
        //console.log("convas width:"+width+",convas height:"+height);


    }
    calculatesize(width){
        let size = (width-50)/4;
        let marginsize = size*0.05;
        let bricksize = size-marginsize*2;
        //console.log("bricksize:"+bricksize+",marginsize:"+marginsize);
        this.setState({bricksize:bricksize,marginsize:marginsize},this.updateprop);
    }
    update_buttonlist(buttonlist,callback){
        this.setState({buttonlist:buttonlist,callback:callback},this.updateprop);
    }
    updateprop(){
        for(let i=0;i<this.state.buttonlist.length;i++) {
            this.refs[this.state.key + i].updateprop(this.state.buttonlist[i],this.state.bricksize,this.state.callback);
            //console.log(this.state.Framelist[i]);
        }
    }
    hide(){
        this.setState({hide:"none"});
    }
    show(){
        this.setState({hide:"block"});
    }
    render() {
        let items = [];
        for(let i=0;i<this.state.buttonlist.length;i++){
            let tempkey = "brick"+i;
                items.push(<div key={this.state.key+i} style={{marginTop:this.state.marginsize,marginLeft:this.state.marginsize,marginRight:this.state.marginsize,marginBottom:this.state.marginsize,width:this.state.bricksize,height:this.state.bricksize,float: "left",position:"relative"}}>
                    <Languagebrick  ref={tempkey}/>
                </div>
                );
        }

        return (
            <div style={{position:"relative",background:"#FFFFFF",height:this.state.height,maxHeight:this.state.height,width:'100%',display:this.state.hide,overflow:'scroll',overflowX:'hidden'}}>
                {items}

            </div>

        );
        /*
         <div className="modal fade" id="NewConfigureModel" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel" style={{height:this.state.height,maxHeight:this.state.height,width:'100%'}}>
         <div className="modal-dialog" role="document">
         <div className="modal-content">
         <div className="modal-header">
         <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
         <h4 className="modal-title" >Please select a configure as base</h4>
         </div>
         <div className="modal-body" style={{overflow:"scroll",overflowX:"hidden"}}>
         <div className="col-md-12">
         <div style={{position:"relative",background:"#FFFFFF",width:'100%',display:this.state.hide}}>
         {baseicons}
         </div>
         <div style={{position:"relative",background:"#FFFFFF",width:'100%',display:this.state.hide}}>
         {conficons}
         </div>
         </div>
         <div className="modal-footer">
         <button type="button" className="btn btn-default" data-dismiss="modal">����</button>
         <button type="button" className="btn btn-primary" id="NewConfigureModuleConfirm" StatCode="">�޸�</button>
         </div>
         </div>
         </div>
         </div>
         </div>


        * */
    }
}