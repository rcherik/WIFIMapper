window.onload = function()
{
	setTimeout(function()
	{
		if (typeof performance !== 'undefined' &&
			typeof performance.timing !== 'undefined' &&
			typeof performance.timing.loadEventEnd !== 'undefined' &&
			typeof performance.timing.responseEnd !== 'undefined')
		{
			var t = performance.timing;
			console.log("Loaded in " +
				((t.loadEventEnd - t.responseEnd) / 1000) +
				" seconds");
		}
	}, 0);
}
