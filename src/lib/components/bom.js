
// export const headers = 'PN,Link,Desc,Qty Req,Price EA,Total,Note'.split(',');
export const headers =  {
    1: 'PN',
    2: 'Link',
    3: 'Desc',
    4: 'Qty',
    5: 'Price',
    6: 'Total',
    7: 'Note'
};

export function makeBomRow(r){
    return {
        1: '',
        2: r.link,
        3: r.Desc,
        4: r.Qty,
        5: r.Price,
        6: r.Price * r.Qty,
        7: ''
    };
};

export const bomData = [
	{
		PN: 'BiHiKu7N',
		Desc: 'Jinko 540w Solar Panel',
		Qty: 4,
		Price: 189,
		ebayid: null,
		link: 'https://www.santansolar.com/product/new-jinko-bifacial-540w-solar-panel-jkm540m-72hl4tv/'
	},
	{
		Desc: "4' Ground Rod With Clamp",
		Qty: 1,
		Price: 40,
		ebayid: 123325099490,
		link: 'https://ebay.us/Zs4BO3'
	},
	{
		Desc: "15' Ground Wire",
		Qty: 1,
		Price: 12,
		ebayid: 292010027574,
		link: 'https://www.ebay.com/itm/292010027574?amdata=enc%3AAQAJAAAAkCi0pTfUJ%2Buf3%2Fer6gVJo6qNgVkIU6pnr0Y%2FpNawJO7iI0pbOjitwms6%2BO%2FA2bNiDKycuRbzdyVM61OHwqGQoGq1d6peNkUZK4jf0MiOvlN3p0YDvMUsAC1p8ZvxwUE%2FmNJzYjcMOQigrtrP%2BnrFlEYjy6buK13TnCFzR8P6ObKyoZ8WkZpF6qyQuGptyjmIXQ%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Solar Grounding Lug',
		Qty: 3,
		Price: 6,
		ebayid: 172025600337,
		link: 'https://www.ebay.com/itm/172025600337?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Shutoff Switch breaker style',
		Qty: 1,
		Price: 44,
		ebayid: 315177701793,
		link: 'https://www.ebay.com/itm/315177701793?amdata=enc%3AAQAJAAAAoGUyaN46%2BaY6awaX57q6yH13V0PaPeNyo4hXTIY68YYel1Hkft33U85%2BvlNZV25pXtVjsL%2BY%2BIkjEhYljj6Hgwlzl7SV%2BsoqJBqmrTzZe11WXxM8%2BVU7XN9Aje0z1fmKzciEczDVKmWrL28kxbqgyKjDAui%2BORyQ2yaqbmESLxMy0qGLgatxPfaz9p2gPlqGeNIe3CnlBRtW8XjSOaI8hkg%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Shutoff Switch twist style',
		Qty: 1,
		Price: 50,
		ebayid: 235459112866,
		link: 'https://www.ebay.com/itm/235459112866?amdata=enc%3AAQAJAAAAkFiv0Ud50QQTRynOA2fzbYo5d5t09o4LBq%2FvResFUX3kzNQ14g4xXuQSvN3DE%2FrTLeIU4lw4ixDHqEf1aOLsOHIlvn6Uz3LzrwHFxp3eGStG4pVtUsxjBM1N4PiiFNclp9eW7qIS63u5D3XLfTUahLXG6WyNXSLUt%2F%2B%2F8Cu9tfUUCwPkzdIN9AQ9MoutgDACmQ%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: '3/4" x 50ft  Flexible Non Metallic Conduit kit',
		Qty: 1,
		Price: 50,
		ebayid: 262383880095,
		link: 'https://www.ebay.com/itm/262383880095?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Solar Mounting Rails',
		Qty: 6,
		Price: 23,
		ebayid: null,
		link: 'https://www.santansolar.com/product/k2-cross-rail-44-x-86-mill/'
	},
	{
		Desc: 'Rail-To-Rail Connector',
		Qty: 4,
		Price: 5,
		ebayid: null,
		link: 'https://www.santansolar.com/product/k2-rail-connector-cross-rail-44-x-mill/'
	},
	{
		Desc: 'Flashing/Mount Kit',
		Qty: 8,
		Price: 9,
		ebayid: null,
		link: 'https://www.santansolar.com/product/k2-everflash-xp-comp-kit-mill/'
	},
	{
		Desc: 'Middle solar clamp bolts',
		Qty: 4,
		Price: 4,
		ebayid: null,
		link: 'https://www.santansolar.com/product/k2-mid-clamp-mil-25-45mm-m8x40/'
	},
	{
		Desc: 'End solar clamp bolts ',
		Qty: 4,
		Price: 4,
		ebayid: null,
		link: 'https://www.santansolar.com/product/k2-end-clamp-silver-25-40mm/'
	},
	{
		Desc: 'Roof to Rail brackets (long for more tilt)',
		Qty: 8,
		Price: 6,
		ebayid: null,
		link: 'https://www.santansolar.com/product/k2-big-foot-6-w-3-chem-link-clip-kit/'
	},
	{
		Desc: 'Stainless Lag bolts for roof mounts',
		Qty: 16,
		Price: 2,
		ebayid: 293494409497,
		link: 'https://www.ebay.com/itm/293494409497?amdata=enc%3AAQAJAAAAkEIqG6O9ynK7abaIuDwtQlMdreHbTGRBwQ8FN3TKYRvrW2JS%2B34NS4TQr%2BSe%2FQWJdTjpiZjLKEeQST%2BGD5EUWRxKuILar62NjluXaaDHMuKmt6kXIriWVWdkcA26oIXdzHuS3I9LDfxkeiOSVbXWG1ckz13Sil05SddN%2BkmG4UolyBGgs%2Bea6uGePsH%2Fbsq4jA%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: '600v 10 AWG black and red solar wire',
		Qty: 100,
		Price: 1.15,
		ebayid: 235018315902,
		link: 'https://www.ebay.com/itm/235018315902?amdata=enc%3AAQAJAAAAkIvrZP3TaXgE3LfBM4e96%2Ffp1u8Ih0gbUDPIRy54B2rAp2pKTo9NlvQ6xD62nzeDLvXacpO8qmWmTIlJ3tkZm%2FBAR38%2FDxtB0FOvuukN5qsVefKlWAjp6K8FBQS7MLiJVwjPjgQR89fY4pXqQoDPQa2cQ8N5QG3LpWvkwIQFNLWi%2FORhT0YJMI%2BLJ9doU6HPiw%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Basic MC4 crimper kit',
		Qty: 1,
		Price: 33,
		ebayid: 186178066931,
		link: 'https://www.ebay.com/itm/186178066931?amdata=enc%3AAQAJAAAAkIuSAkIcxfB8CrAO%2FrkTPdjMbwXWYOVO%2B86MC3L5JmPdD4PG%2B%2B7oPJqsXK9IM9RegHDuwaCLOa7GwsRu9EpJWR6qJEqVC4H1WuapGDcEAw9tO3FsMKLrr1mwa%2BEpXMuZWaUDHtso3pT4E%2FqzNIfmfe5j3wY0crB4Sdcu60HYc3rjjAowD6stKyJ6FEZ2h4b8aA%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	// {
	//     "Desc": "Fancy MC4 crimper kit",
	//     "Qty": 1,
	//     "Price": 95,
	//     "ebayid": 273483825968
	// },
	{
		Desc: 'Thermostatic Mixing Valve',
		Qty: 1,
		Price: 50,
		ebayid: 163916404115,
		link: 'https://www.ebay.com/itm/163916404115?mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Misc copper fittings/elbows',
		Qty: 6,
		Price: 4,
		ebayid: null,
		link: ''
	},
	{
		Desc: '120V 2000W 7.2Ω Water Heater Element ',
		Qty: 1,
		Price: 37,
		ebayid: 186398059270,
		link: 'https://www.ebay.com/itm/186398059270?amdata=enc%3AAQAJAAAAkKg0quUQ2k8hDNt7%2FIcBHA57QU8p6MjHQ%2BrCF%2F2AkRl%2BM7fOguWz4rKuoPv171WUp2xHMiRY%2FzpD%2FUM4qcBAR0Zliv5aL4Y3rIPY83FXvPxYRJh%2BfhMu7MGPAyPHj0oeTHioFRNzcEGXplc%2Fy6CqPlzM08UX%2B%2Fsbjubl7A5GnGahPKIuwPrR2nSQuj2nxY9%2BxA%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'Heater Element Wrench',
		Qty: 1,
		Price: 30,
		ebayid: 333850374625,
		link: 'https://www.ebay.com/itm/333850374625?amdata=enc%3AAQAJAAAAkK%2BR7XoIhkFRcqg1voAaiy5MZJ9qa7grF%2FUXLBQj9iEzNnGjfpl70B0Cbbilpnb4PxHTcTzrxIH1FKX6uBxG6OwgzOnVXOi6QI60wqD5SRJ6ioOAglD%2BA4Rnn%2F0UjxnzQOPVdOvYJnH8nG9XMgcVSOraFpmkPxmFupleq3Rbt3ivKIVTBNZwhJngkw%2FDKamaoQ%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'DC 0-300V Meter ',
		Qty: 1,
		Price: 26,
		ebayid: 145519750249,
		link: 'https://www.ebay.com/itm/145519750249?amdata=enc%3AAQAJAAAAkNAqMZmoSe2aAbjzc333%2BfvHwvSRWxO8w4rV98Gua8xHrDmKOyx0wDwpwWXV0QSj3dkgi1JnsgAlPR49ByaMVhu4Mj8bXgnQ17HufwGopYCY3oce86pTWmW0uuzr8nEBrV8pR0WH0vLjmm0NuWcuzlzSgaOYpG4PeuYuXTBQ0qvxtel71VKVPdx0JcLxHt0NTw%3D%3D&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339056755&customid=&toolid=10001&mkevt=1'
	},
	{
		Desc: 'MPPT Boiler PV Solar Regulator',
		Qty: 1,
		Price: 370,
		ebayid: 263523458861,
		link: 'https://www.ebay.com/itm/265624377737'
	}
];
