const say = (...msgs) => console.log(...msgs);


const rfuncs = {};


async function sendmsg(data) {
	const response = fetch('/test', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			data
		})
	})
	.then(response => response.json())
	.then(data => getmsg(data))
	.catch(error => console.error('Error sending data:', error));
}


function getmsg(data) {
	if (data['t'] in rfuncs) {
		rfuncs[data['t']](data);
	}
	else { say('no js handler for ' + data['t']); }
}


function test() {
    sendmsg({t: 'test'});
}
rfuncs['test'] = function(data) {
    console.log(data)
}


$(".testbutton").click(function() {
	sendmsg({t: 'test'});
})
rfuncs['test'] = function(data) {
	say(data);
}

