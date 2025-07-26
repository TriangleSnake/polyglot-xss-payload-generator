var lst = []
document.querySelectorAll("a").forEach((e)=>{
    fetch(e.href).then(res=>res.text()).then(html=>{
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");
        doc.querySelectorAll("a").forEach(e=>console.log(e.href))
    })
})