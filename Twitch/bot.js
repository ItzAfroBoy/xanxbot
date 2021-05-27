const fs = require('fs');
const tmi = require('tmi.js');
const helper = require('./helper');

const cmdCollection = fs.readdirSync('./commands').filter((file) => file.endsWith('.js'));
let commands = [];
let opts = {
	identity: {
		username: helper.username,
		password: helper.password
	},
	channels: helper.channels
};

function onMessage(channel, ctx, msg, self) {
	if (self || !msg) return;

	const args = msg.slice(1).split(' ');
	const command = args.shift().toLowerCase();

	if (commands.indexOf(command) >= 0) {
		let x = commands.indexOf(command);
		commands[x + 1](channel, ctx, msg, self, client);
	}
}

function onConnected (addr, port) {
	console.log(`[+] Connected to ${addr}:${port}`);
	console.log(`[+] Currently in ${channels.length} channels as ${username}`);
}

for (const file of cmdCollection) {
	let x = file.split('.');
	let name = x[0];
	let i = require(`./commands/${name}`);
	commands.push(name, i.execute);
}

const client = new tmi.client(opts);
client.connect();
client.on('message', onMessage);
client.on('connected', onConnected);
