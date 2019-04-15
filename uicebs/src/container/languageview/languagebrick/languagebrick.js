/**
 * Created by hyj on 2016/12/22.
 */

import React, {
    Component,
    PropTypes
    } from 'react';

import classNames from 'classnames';
import "./languagebrick.css"
import '../../../../resource/css/font-awesome.min.css';
export default class languagebrick extends Component {

    constructor(props) {
        super(props);
        let default_conf = {
            "name":"CHINESE",
            "icon":"China.svg",
            "abbreviation":"ch"
        }
        this.state = {
            bricksize:800,
            configuration:default_conf,
            callback:null
        };
    }
    updateprop(configuration,bricksize,callback){
        this.setState({configuration:configuration,bricksize:bricksize,callback:callback});
    }
    handle_click(){
        //console.log("click");
        this.state.callback(this.state.configuration);
    }
    render() {
        let icon = "./flag/"+this.state.configuration.icon;
        let name = this.state.configuration.name;
        return (
            <div  style={{position:"relative",flex:1,width:this.state.bricksize,boxShadow:"5px 5px 5px #DDDDDD",background:"#DDDDDD"}} >
                <button type="button" className="btn" style={{height:this.state.bricksize,width:this.state.bricksize,verticalAlign:"middle"}} onClick={this.handle_click.bind(this)}><i>
                    <img src={icon}  style={{height:this.state.bricksize*0.4,width:this.state.bricksize*0.6,marginTop:this.state.bricksize*0.2}}></img><br/>
                    <a style={{position:"relative",height:this.state.bricksize*0.3,display:'table-cell',verticalAlign:'middle'}}>
                        <span className="framelabel"  style={{fontSize:this.state.bricksize*0.1,marginLeft:0}}>
                            {name}
                        </span>
                    </a>

                </i></button>
            </div>
        );
    }
}