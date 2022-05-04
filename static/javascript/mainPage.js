// document.getElementById("convert2Img").onclick = function () {
//     const screenshotTarget = document.getElementById("timeTable");
//     html2canvas(screenshotTarget).then((canvas) => {
//         const base64Image = canvas.toDataURL("image/png");
//         var anchor = document.createElement("a");
//         anchor.setAttribute("href", base64Image);
//         anchor.setAttribute("download", "Time Table.png");
//         anchor.click();
//         anchor.remove();
//     });
// };

function downloadTimeTable() {
    var node = document.getElementById('timeTable');
    domtoimage.toPng(node)
        .then(function (dataUrl) {
            var img = new Image();
            img.src = dataUrl;
            downloadURI(dataUrl, "TKB.png")
        })
}

function downloadURI(uri, name) {
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}

// $(document).ready(function () {
//     $("#convert2Img").click(function () {
//         domtoimage.toBlob(document.getElementById("timeTable"))
//             .then(function (blob) {
//                 window.saveAs(blob, "TKB.png")
//             })
//     })
// })