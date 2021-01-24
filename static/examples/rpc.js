async function* readLines(response) {
    let reader = response.body.getReader();
    let decoder = new TextDecoder();
    let buffer = '';

    do {
        var { done, value } = await (reader.read());
        value = decoder.decode(value);
        buffer += value;
        let lines = buffer.split('\n');
        buffer = lines.pop();
        for (line of lines) {
            yield line;
        }
    } while (!done);

    yield buffer;
}

async function readWithProgress(response, progressCallback) {
    let status = 0;
    let result = '';
    for await (let line of readLines(response)) {
        if (line === 'done') {
            status = 1;
        } else if (line === 'failed') {
            status = 2;
        } else {
            if (status === 0) {
                progressCallback(parseFloat(line));
            } else {
                result += line;
            }
        }
    }

    if (status === 1) {
        return result;
    } else {
        throw new Error(result);
    }
}

async function call(url, data, progressCallback) {
    let response = await fetch(url, { method: 'POST', body: data });
    return  await readWithProgress(response, (p) => {
        progressCallback(p)
    });
}