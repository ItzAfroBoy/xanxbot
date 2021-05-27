exports.execute = (channel, ctx, msg, self, client) => {
	const sides = 6;
	return client.say(channel, Math.floor(Math.random() * sides)) + 1;
};