function downloadTimeTable() {
    const node = document.getElementById('timeTable');
    domtoimage.toPng(node)
        .then(function (dataUrl) {
            const img = new Image();
            img.src = dataUrl;
            downloadURI(dataUrl, "TKB.png")
        })
}

function downloadURI(uri, name) {
    let link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}