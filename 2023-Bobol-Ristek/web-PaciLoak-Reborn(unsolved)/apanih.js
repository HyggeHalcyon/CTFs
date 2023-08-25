// ....

app.post(`/order`, async (req, res) => {
    let orderInsensitive = req.body.order.toLowerCase();
    let blacklist = [`script`, `img`, `src`, `.`, `[`, `]`, `onerror`, `onmouseover`, `onclick`, `onload`, `fetch`, `xml`];
    for(let token of blacklist)
        if(orderInsensitive.includes(token))
            return res.render(`forbidden`);

    reviewQueue.push(req.body.order);
    check(req.baseUrl);
    res.render(`thanks`);
});

// ....