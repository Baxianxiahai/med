var perimeters = window.location.search;
var div1 = document.getElementById("2_answer_1");
layui.use(['form', 'layedit', 'laydate'], function() {
	var form = layui.form,
		layer = layui.layer,
		layedit = layui.layedit,
		laydate = layui.laydate;
	//日期
	
	lay('.test-item').each(function() {
		laydate.render({
			elem: this,
			trigger: 'click'
		});
	});
	//创建一个编辑器
	var editIndex = layedit.build('LAY_demo_editor');
	//自定义验证规则
	form.verify({
		name: function(value) {
			if(value.length < 1) {
				return '请输入姓名';
			}
		},
		address: function(value) {
			if(value.length < 1) {
				return '请输入居住地址';
			}
		},
		IDcard: [/(^\d{15}$)|(^\d{17}([0-9]|X)$)/, '请输入正确的身份证号'],
		age: [/^[0-9]{1,2}$/, '请输入正确的年龄'],
		telphone: [/^[1][3,5,8][0-9]{9}$/, '请输入正确的手机号'],
	});
	//监听提交
	//	form.on('submit(index)', function(data) {
	//		var list = document.getElementsByName("index_sex");
	//		for(i = 0; i < list.length; i++) {
	//			if(list[i].checked == true) {
	//				if(list[i].value == "女") {
	//					window.location.href = 'woman.html';
	//				} else {
	//					window.location.href = 'man.html';
	//				}
	//			}
	//		}
	//		return false;
	//	});
	form.on('submit(index_1)', function(data) {
		layer.alert(JSON.stringify(data.field), {
			title: '最终的提交信息'
		})
		window.location.href = "index.html";
		return false;
	});
	form.on('submit(second_1)', function(data) {
		var params1 = $("#case1111").serializeJSON();
		console.log(params1);
		console.log(JSON.stringify(params1));
		window.location.href = "index.html";
		return false;
	});
	form.on('submit(third_1)', function(data) {
		window.location.href = "third_2.html";
		return false;
	});
	form.on('submit(third_2)', function(data) {
		window.location.href = "third_3.html";
		return false;
	});
	form.on('submit(third_3)', function(data) {
		window.location.href = "third_4.html";
		return false;
	});
	form.on('submit(third_4)', function(data) {
		window.location.href = "third_5.html";
		return false;
	});
	form.on('submit(third_5)', function(data) {
		window.location.href = "third_6.html";
		return false;
	});
	form.on('submit(third_6)', function(data) {
		window.location.href = "index.html";
		return false;
	});
	form.on('submit(fourth_1)', function(data) {
		window.location.href = "fourth_2.html";
		return false;
	});
	//	form.on('submit(common_3)', function(data) {
	//		window.location.href = "common_4.html";
	//		return false;
	//	});
	//	form.on('submit(common_4)', function(data) {
	//		window.location.href = "common_6.html";
	//		return false;
	//	});
	//	form.on('submit(common_6)',function(data){
	//		window.location.href="common_5.html";
	//		return false;
	//	});
	//	form.on('submit(common_6)', function(data) {
	//		layer.alert("调查结束，返回首页", {
	//				title: "消息提示"
	//			},
	//			function() {
	//				window.location.href = "main.html";
	//				//return false;
	//			})
	//		return false;
	//	});
	//	form.on('submit(demo1)', function(data) {
	//		layer.alert(JSON.stringify(data.field), {
	//			title: "最终提交消息"
	//		});
	//		return false;
	//	});
	//	form.on('submit(lumbago_1)', function(data) {
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(obj['lumbago_1_answer1']) + parseInt(obj["lumbago_1_answer2"]) + parseInt(obj["lumbago_1_answer3"]) + parseInt(obj["lumbago_1_answer4"]) + parseInt(obj["lumbago_1_answer5"]) + parseInt(obj["lumbago_1_answer6"]) + parseInt(obj["lumbago_1_answer7"]) + parseInt(obj["lumbago_1_answer8"]) + parseInt(obj["lumbago_1_answer9"]) + parseInt(obj["lumbago_1_answer10"]);
	//		layer.alert(String(s), {
	//			title: '最终得分'
	//		}, function() {
	//			window.location.href = "main.html";
	//		})
	//		return false;
	//	});
	//	form.on('submit(balance)', function(data) {
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(obj['balance_answer1']) + parseInt(obj["balance_answer2"]) + parseInt(obj["balance_answer3"]) + parseInt(obj["balance_answer4"]) + parseInt(obj["balance_answer5"]) + parseInt(obj["balance_answer6"]) + parseInt(obj["balance_answer7"]) + parseInt(obj["balance_answer8"]) + parseInt(obj["balance_answer9"]) + parseInt(obj["balance_answer10"]) + parseInt(obj["balance_answer11"]) + parseInt(obj["balance_answer12"]) + parseInt(obj["balance_answer13"]) + parseInt(obj["balance_answer14"]);
	//		layer.alert(String(s), {
	//			title: '最终得分'
	//		}, function() {
	//			window.location.href = "main.html";
	//		})
	//		return false;
	//	});
	//	form.on('submit(SF_36_1)', function(data) {
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(obj['SF_36_1_answer1']) + parseInt(obj["SF_36_1_answer2"]) + parseInt(obj["SF_36_1_answer3"]) + parseInt(obj["SF_36_1_answer4"]) + parseInt(obj["SF_36_1_answer5"]) + parseInt(obj["SF_36_1_answer6"]) + parseInt(obj["SF_36_1_answer7"]);
	//		window.location.href = "SF_36_2.html?" + s;
	//		console.log(s);
	//		return false;
	//	});
	//	form.on('submit(SF_36_2)', function(data) {
	//		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(perimeters) + parseInt(obj['SF_36_2_answer1']) + parseInt(obj["SF_36_2_answer2"]) + parseInt(obj["SF_36_2_answer3"]) + parseInt(obj["SF_36_2_answer4"]) + parseInt(obj["SF_36_2_answer5"]) + parseInt(obj["SF_36_2_answer6"]) + parseInt(obj["SF_36_2_answer7"]) + parseInt(obj["SF_36_2_answer8"]) + parseInt(obj["SF_36_2_answer9"]);
	//		window.location.href = "SF_36_3.html?" + s;
	//		console.log(s);
	//		return false;
	//	});
	//	form.on('submit(SF_36_3)', function(data) {
	//		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(perimeters) + parseInt(obj['SF_36_3_answer1']) + parseInt(obj["SF_36_3_answer2"]) + parseInt(obj["SF_36_3_answer3"]) + parseInt(obj["SF_36_3_answer4"]) + parseInt(obj["SF_36_3_answer5"]) + parseInt(obj["SF_36_3_answer6"]);
	//		window.location.href = "SF_36_4.html?" + s;
	//		console.log(s);
	//		return false;
	//	});
	//	form.on('submit(SF_36_4)', function(data) {
	//		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(perimeters) + parseInt(obj['SF_36_4_answer1']) + parseInt(obj["SF_36_4_answer2"]) + parseInt(obj["SF_36_4_answer3"]) + parseInt(obj["SF_36_4_answer4"]) + parseInt(obj["SF_36_4_answer5"]) + parseInt(obj["SF_36_4_answer6"]) + parseInt(obj["SF_36_4_answer7"]) + parseInt(obj["SF_36_4_answer8"]) + parseInt(obj["SF_36_4_answer9"]);
	//		window.location.href = "SF_36_5.html?" + s;
	//		console.log(s);
	//		return false;
	//	});
	//	form.on('submit(SF_36_5)', function(data) {
	//		perimeters = decodeURI(perimeters.substr(1).split('&')[0]);
	//		var jsonstr = JSON.stringify(data.field);
	//		var obj = JSON.parse(jsonstr);
	//		var s = parseInt(perimeters) + parseInt(obj['SF_36_5_answer1']) + parseInt(obj["SF_36_5_answer2"]) + parseInt(obj["SF_36_5_answer3"]) + parseInt(obj["SF_36_5_answer4"]) + parseInt(obj["SF_36_5_answer5"]);
	//		layer.alert(s, {
	//			title: 'SF_36量表最终得分'
	//		}, function() {
	//			window.location.href = "main.html";
	//		});
	//		return false;
	//	});
	form.on('radio(2_answer_1)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "甲状旁腺功能亢进症",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_1'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_1").style.display = 'none';
				}
			});
		}
		//		else{
		//			$("#2_answer_1").load(location.href+' #2_answer_1');
		//			document.getElementById("2_answer_1").style.display = 'none';
		//		}
	});
	form.on('radio(2_answer_2)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "垂体前叶功能减退症",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_2'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_2").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_3)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "早绝经",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_3'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_3").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_4)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "库欣综合征",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_4'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_4").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_5)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "性腺功能减退症",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_5'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_5").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_6)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "糖尿病（1型及2型）",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_6'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_6").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_7)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "甲状腺功能亢进症",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_7'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_7").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_8)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "神经性厌食",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_8'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_8").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_9)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "雄激素抵抗综合征",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_9'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_9").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_10)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "炎性肠病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_10'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_10").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_11)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "胃肠道旁路或其他手术",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_11'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_11").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_12)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "原发性胆汁性肝硬化",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_12'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_12").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_13)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "胰腺疾病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_13'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_13").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_14)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "乳糜泻",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_14'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_14").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_15)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "吸收不良",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_15'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_15").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_16)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "多发性骨髓瘤",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_16'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_16").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_17)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "白血病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_17'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_17").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_18)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "淋巴瘤",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_18'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_18").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_19)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "单克隆免疫球蛋白病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_19'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_19").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_20)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "血友病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_20'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_20").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_21)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "镰状细胞贫血",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_21'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_21").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_22)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "系统性肥大细胞增多症",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_22'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_22").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_23)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "球蛋白生成障碍性贫血",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_23'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_23").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_24)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "类风湿关节炎",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_24'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_24").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_25)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "系统性红斑狼疮",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_25'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_25").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_26)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "强直性脊柱炎",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_26'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_26").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_27)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "其他风湿免疫性疾病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_27'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_27").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_28)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "癫痫",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_28'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_28").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_29)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "卒中",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_29'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_29").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_30)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "肌萎缩",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_30'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_30").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_31)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "帕金森病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_31'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_31").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_32)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "脊髓损伤",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_32'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_32").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_33)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "慢性代谢性酸中毒",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_33'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_33").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_34)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "终末期肾病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_34'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_34").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_35)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "器官移植后遗症",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_35'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_35").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_36)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "慢性阻塞性肺病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_36'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_36").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_37)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "充血性心衰",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_37'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_37").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_38)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "结节病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_38'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_38").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_39)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "特发性脊柱侧凸",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_39'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_39").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_40)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "抑郁",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_40'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_40").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_41)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "肠外营养",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_41'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_41").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_42)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "淀粉样变",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_42'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_42").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_43)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "艾滋病",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_43'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_43").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_44)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "前列腺癌的药物",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_44'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_44").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_45)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "抗凝血剂（肝素）",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_45'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_45").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_46)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "抗癫痫药",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_46'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_46").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_47)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "芳香酶抑制剂",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_47'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_47").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_48)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "环孢素A和他克莫司",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_48'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_48").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_49)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "癌症化疗药物",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_49'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_49").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_50)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "糖皮质激素",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_50'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_50").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_51)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "促性腺激素释放激素激动剂",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_51'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_51").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_52)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "铝剂（抑酸剂）",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_52'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_52").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_53)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "质子泵抑制剂",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_53'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_53").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_54)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "选择性血清素再摄取抑制剂（SSRIs）",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_54'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_54").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_55)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "甲状腺素",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_55'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_55").style.display = 'none';
				}
			});
		}
	});
	form.on('radio(2_answer_56)', function(data) {
		if(data.value == "1") {
			layer.open({
				type: 1,
				area: ['300px', '500px'],
				title: "抗病毒药物",
				closeBtn: 0,
				btn: ['确定'],
				content: $('#2_answer_56'),
				btn1: function() {
					layer.closeAll();
					document.getElementById("2_answer_56").style.display = 'none';
				}
			});
		}
	});
});
layui.use('upload', function() {
	var $ = layui.jquery,
		upload = layui.upload;
	//多文件列表示例
	var demoListView = $('#demoList'),
		uploadListIns = upload.render({
			elem: '#testList',
			url: '/upload/',
			accept: 'file',
			multiple: true,
			auto: false,
			bindAction: '#testListAction',
			choose: function(obj) {
				var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
				//读取本地文件
				obj.preview(function(index, file, result) {
					var tr = $(['<tr id="upload-' + index + '">', '<td>' + file.name + '</td>', '<td>', '<button class="layui-btn layui-btn-mini demo-reload layui-hide">重传</button>', '<button class="layui-btn layui-btn-mini layui-btn-danger demo-delete">删除</button>', '</td>', '</tr>'].join(''));

					//单个重传
					tr.find('.demo-reload').on('click', function() {
						obj.upload(index, file);
					});

					//删除
					tr.find('.demo-delete').on('click', function() {
						delete files[index]; //删除对应的文件
						tr.remove();
						uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
					});

					demoListView.append(tr);
				});
			},
			done: function(res, index, upload) {
				if(res.code == 0) { //上传成功
					var tr = demoListView.find('tr#upload-' + index),
						tds = tr.children();
					tds.eq(1).html(''); //清空操作
					return delete this.files[index]; //删除文件队列已经上传成功的文件
				}
				this.error(index, upload);
			},
			error: function(index, upload) {
				var tr = demoListView.find('tr#upload-' + index),
					tds = tr.children();
				tds.eq(1).find('.demo-reload').removeClass('layui-hide'); //显示重传
			}
		});
});