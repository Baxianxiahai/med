var perimeters = window.location.search;
layui.use(['form', 'layedit', 'laydate'], function(){
	var form = layui.form
	,layer = layui.layer
	,layedit = layui.layedit
	,laydate = layui.laydate;
	//日期
	laydate.render({
		elem: '#date'
	});
	laydate.render({
		elem: '#date1'
	});
	//创建一个编辑器
	var editIndex = layedit.build('LAY_demo_editor');
	//自定义验证规则
	form.verify({
		name: function(value){
			if(value.length <1){
				return '请输入姓名';
			}
		},
		address: function(value){
			if(value.length <1){
				return '请输入居住地址';
			}
		},
		IDcard:[/(^\d{15}$)|(^\d{17}([0-9]|X)$)/,'请输入正确的身份证号'],
		age:[/^[0-9]{1,2}$/,'请输入正确的年龄'],
		telphone:[/^[1][3,5,8][0-9]{9}$/,'请输入正确的手机号'],
	});
	//监听提交
	form.on('submit(index)', function(data){
		var list=document.getElementsByName("index_sex");
		for(i=0;i<list.length;i++){
			if(list[i].checked==true){
				if(list[i].value=="女"){
					window.location.href='woman.html';
				}
				else{
					window.location.href='man.html';
				}
			}
		}
		return false;
	});
	form.on('submit(man)',function(data){
		window.location.href="common_1.html";
		return false;
	});
	form.on('submit(woman)',function(data){
		window.location.href="common_1.html";
		return false;
	});
	form.on('submit(common_1)',function(data){
		window.location.href="common_2.html";
		return false;
	});
	form.on('submit(common_2)',function(data){
		window.location.href="common_3.html";
		return false;
	});
	form.on('submit(common_3)',function(data){
		window.location.href="common_4.html";
		return false;
	});
	form.on('submit(common_4)',function(data){
		window.location.href="common_6.html";
		return false;
	});
//	form.on('submit(common_6)',function(data){
//		window.location.href="common_5.html";
//		return false;
//	});
	form.on('submit(common_6)',function(data){
		layer.alert("调查结束，返回首页",{title:"消息提示"},
		function(){
			window.location.href="main.html";
			//return false;
		})
		return false;
	});
	form.on('submit(demo1)',function(data){
		layer.alert(JSON.stringify(data.field),{title:"最终提交消息"});
		return false;
	});
	form.on('submit(lumbago_1)',function(data){
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(obj['lumbago_1_answer1'])+parseInt(obj["lumbago_1_answer2"])+parseInt(obj["lumbago_1_answer3"])+parseInt(obj["lumbago_1_answer4"])+parseInt(obj["lumbago_1_answer5"])+parseInt(obj["lumbago_1_answer6"])+parseInt(obj["lumbago_1_answer7"])+parseInt(obj["lumbago_1_answer8"])+parseInt(obj["lumbago_1_answer9"])+parseInt(obj["lumbago_1_answer10"]);
		layer.alert(String(s), {
			title: '最终得分'
		},function(){
			window.location.href="main.html";
		})
		return false;
	});
	form.on('submit(balance)',function(data){
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(obj['balance_answer1'])+parseInt(obj["balance_answer2"])+parseInt(obj["balance_answer3"])+parseInt(obj["balance_answer4"])+parseInt(obj["balance_answer5"])+parseInt(obj["balance_answer6"])+parseInt(obj["balance_answer7"])+parseInt(obj["balance_answer8"])+parseInt(obj["balance_answer9"])+parseInt(obj["balance_answer10"])+parseInt(obj["balance_answer11"])+parseInt(obj["balance_answer12"])+parseInt(obj["balance_answer13"])+parseInt(obj["balance_answer14"]);
		layer.alert(String(s), {
			title: '最终得分'
		},function(){
			window.location.href="main.html";
		})
		return false;
	});
	form.on('submit(SF_36_1)',function(data){
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(obj['SF_36_1_answer1'])+parseInt(obj["SF_36_1_answer2"])+parseInt(obj["SF_36_1_answer3"])+parseInt(obj["SF_36_1_answer4"])+parseInt(obj["SF_36_1_answer5"])+parseInt(obj["SF_36_1_answer6"])+parseInt(obj["SF_36_1_answer7"]);
		window.location.href="SF_36_2.html?"+s;
		console.log(s);
		return false;
	});
	form.on('submit(SF_36_2)',function(data){
		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(perimeters)+parseInt(obj['SF_36_2_answer1'])+parseInt(obj["SF_36_2_answer2"])+parseInt(obj["SF_36_2_answer3"])+parseInt(obj["SF_36_2_answer4"])+parseInt(obj["SF_36_2_answer5"])+parseInt(obj["SF_36_2_answer6"])+parseInt(obj["SF_36_2_answer7"])+parseInt(obj["SF_36_2_answer8"])+parseInt(obj["SF_36_2_answer9"]);
		window.location.href="SF_36_3.html?"+s;
		console.log(s);
		return false;
	});
	form.on('submit(SF_36_3)',function(data){
		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(perimeters)+parseInt(obj['SF_36_3_answer1'])+parseInt(obj["SF_36_3_answer2"])+parseInt(obj["SF_36_3_answer3"])+parseInt(obj["SF_36_3_answer4"])+parseInt(obj["SF_36_3_answer5"])+parseInt(obj["SF_36_3_answer6"]);
		window.location.href="SF_36_4.html?"+s;
		console.log(s);
		return false;
	});
	form.on('submit(SF_36_4)',function(data){
//		var perimeters = window.location.search;
		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(perimeters)+parseInt(obj['SF_36_4_answer1'])+parseInt(obj["SF_36_4_answer2"])+parseInt(obj["SF_36_4_answer3"])+parseInt(obj["SF_36_4_answer4"])+parseInt(obj["SF_36_4_answer5"])+parseInt(obj["SF_36_4_answer6"])+parseInt(obj["SF_36_4_answer7"])+parseInt(obj["SF_36_4_answer8"])+parseInt(obj["SF_36_4_answer9"]);
		window.location.href="SF_36_5.html?"+s;
		console.log(s);
		return false;
	});
	form.on('submit(SF_36_5)',function(data){
		//var perimeters = window.location.search;
		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
		var jsonstr=JSON.stringify(data.field);
		var obj=JSON.parse(jsonstr);
		var s=parseInt(perimeters)+parseInt(obj['SF_36_5_answer1'])+parseInt(obj["SF_36_5_answer2"])+parseInt(obj["SF_36_5_answer3"])+parseInt(obj["SF_36_5_answer4"])+parseInt(obj["SF_36_5_answer5"]);
		layer.alert(s, {
			title: 'SF_36量表最终得分'	
		},function(){
				window.location.href="main.html";
			});
		return false;
	});
});
layui.use('upload', function(){
  var $ = layui.jquery
  ,upload = layui.upload;
  //多文件列表示例
  var demoListView = $('#demoList')
  ,uploadListIns = upload.render({
    elem: '#testList'
    ,url: '/upload/'
    ,accept: 'file'
    ,multiple: true
    ,auto: false
    ,bindAction: '#testListAction'
    ,choose: function(obj){   
      var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
      //读取本地文件
      obj.preview(function(index, file, result){
        var tr = $(['<tr id="upload-'+ index +'">'
          ,'<td>'+ file.name +'</td>'
          ,'<td>'
            ,'<button class="layui-btn layui-btn-mini demo-reload layui-hide">重传</button>'
            ,'<button class="layui-btn layui-btn-mini layui-btn-danger demo-delete">删除</button>'
          ,'</td>'
        ,'</tr>'].join(''));
        
        //单个重传
        tr.find('.demo-reload').on('click', function(){
          obj.upload(index, file);
        });
        
        //删除
        tr.find('.demo-delete').on('click', function(){
          delete files[index]; //删除对应的文件
          tr.remove();
          uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
        });
        
        demoListView.append(tr);
      });
    }
    ,done: function(res, index, upload){
      if(res.code == 0){ //上传成功
        var tr = demoListView.find('tr#upload-'+ index)
        ,tds = tr.children();
        tds.eq(1).html(''); //清空操作
        return delete this.files[index]; //删除文件队列已经上传成功的文件
      }
      this.error(index, upload);
    }
    ,error: function(index, upload){
      var tr = demoListView.find('tr#upload-'+ index)
      ,tds = tr.children();
      tds.eq(1).find('.demo-reload').removeClass('layui-hide'); //显示重传
    }
  });
});