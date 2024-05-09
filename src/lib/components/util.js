export function round(num) {
	var m = Number((Math.abs(num) * 100).toPrecision(15));
	return (Math.round(m) / 100) * Math.sign(num);
}

export function tokWh(j) {
	//converts joules to kwh
	return j / 3600e3;
}

export function vpToR(v, pwr) {
	//converts joules to kwh
	return (v * v) / pwr;
}

export function clamp(value, min, max) {
	if (value < min) return min;
	if (value > max) return max;
	return value;
}
