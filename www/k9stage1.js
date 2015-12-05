/* Stage 1 - remote K9 control */

var ws = null;
var alive = false;

/* Next lines added as minimum camera preview */
var mjpeg_img;
 
function reload_img () {
  mjpeg_img.src = "cam_pic.php?time=" + new Date().getTime();
}
function error_img () {
  setTimeout("mjpeg_img.src = 'cam_pic.php?time=' + new Date().getTime();", 100);
}
function init() {
  mjpeg_img = document.getElementById("mjpeg_dest");
  mjpeg_img.onload = reload_img;
  mjpeg_img.onerror = error_img;
  reload_img();
}

/* Main k9 functions follow */

function connect() {
  ws = new WebSocket("ws://www.XXX.XXX.XXX:XXXX/admin/ws/k9");
  ws.onopen = function(evt){ws.send('{"type":"information", "command":"Command circuit established"}');};
  ws.onclose = function(evt){ws.send('{"type":"information", "command":"Command circuit closed"}');};
  ws.onmessage = function(evt){ distance(evt);};
  sb = new WebSocket("ws://XXX.XXX.XXX.XXX:XXXX/admin/ws/status");
  sb.onopen = function(evt){sb.send('{"type":"information", "command":"K9 feedback established"}'); alive=true;};
  sb.onclose = function(evt){sb.send('{"type":"information", "command":"K9 feedback ended"}'); alive=false;};
  sb.onmessage = function(evt){speed(evt);};
  setInterval(function () {browserAlive();},250);
}

function browserAlive() {
	var message = '{"type":"navigation", "command":"alive"}';
	ws.send(message);
	}

function distance(evt){
	var gap = JSON.parse(evt.data);
	gap = parseInt(gap.payload,[10]);
	if (gap > 50) {
      gap = 50;
		}
	var red = 255-(gap*5);
	var green = 5*gap;
	gap = rgb(red,green,0);
	$('#forward_sensor').css('background-color',gap);
	}
			
function rgb(r, g, b){
  return "rgb("+r+","+g+","+b+")";
}

/* Functions and event handlers for the motors page */

$(document).on("pagecreate","#pg_motor",function(event){

var joystick = new VirtualJoystick({
	container : document.getElementById('joystickcontainer'),
	mouseSupport : true,
	});
	
joystick.addEventListener('touchStart', function(){
	console.log('down')
})

joystick.addEventListener('touchEnd', function(){
	console.log('up')
})

var joystickinterval = setInterval(function () {joystickTick()},100);

function joystickTick(){
	var X = 0;
	var Y = 0;
	X = joystick.deltaX();
	Y = joystick.deltaY()*-1;
	if (X > 100) {X = 100};
	if (X < -100) {X = -100};
	if (Y > 100) {Y = 100};
	if (Y < -100) {Y = -100};
	var message = '{"type":"navigation", "command":"move", "steering": "' + X + '", "motorspeed":"' + Y + '"}';
	ws.send(message); 
}

});

/* Functions and event handlers called on the initialisation of each page */

$(document).on('pageinit', function(){

connect();

document.ontouchmove = function(event){
    event.preventDefault();
}

$('.togglesw').unbind('change').change(function(){
	if($(this).is(":checked"))
		{
		var status = "on";
		}
	else {
		var status = "off";
		}
	var message = '{"type":"toggle", "object":"' + this.id + '", "status":"' + status + '"}';
	ws.send(message);
});

$('#head').unbind('change').change(function(){
  if($(this).val()=="up")
       {
		var status = "up";
       }
  else {
    	var status = "down";
       }
   	var message = '{"type":"toggle", "object":"head", "status":"' + status + '"}';
	ws.send(message);    
});

$('#tail').unbind('change').change(function(){
  if($(this).val()=="up")
       {
		var status = "up";
       }
  else {
    	var status = "down";
       }
   	var message = '{"type":"toggle", "object":"tail", "status":"' + status + '"}';
	ws.send(message);    
});

$('.mood_but').unbind('click').click(function(){
	var message = '{"type":"mood", "object":"' + this.id + '"}';
	ws.send(message);
});

$('#servo_send').unbind('click').click(function(){
	var message = '{"type":"servo", "object":"' + $('#servo_choice option:selected').val() + '", "value":"' + $('#servo_pulse').slider().val() + '"}';
	ws.send(message);
});

});