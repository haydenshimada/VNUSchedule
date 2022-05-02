document.getElementById("convert2Img").onclick = function () {
    const screenshotTarget = document.getElementById("timeTable");
    html2canvas(screenshotTarget).then((canvas) => {
        const base64Image = canvas.toDataURL("image/png");
        var anchor = document.createElement("a");
        anchor.setAttribute("href", base64Image);
        anchor.setAttribute("download", "Time Table.png");
        anchor.click();
        anchor.remove();
    });
};