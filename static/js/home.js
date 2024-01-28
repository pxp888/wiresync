

const newpeerSectionHead = $("#newpeerSectionHead")
const newpeerSection = $("#newpeerSection")
const peerlistHead = $("#peerlistHead")
const peerlist = $("#peerlist")
const entries = $(".peerlistEntries p")


function toggleNewPeerSection() {
    newpeerSection.toggle()
}

function togglePeerSection() {
    peerlist.toggle()
}

function entryfill(event) {
    kids = event.target.parentElement.children;
    fields = $(".inputForm input");
    for (let i = 0; i < kids.length; i++) {
        fields[i+1].value = kids[i].innerHTML;
    }
}

entries.click(entryfill)
newpeerSectionHead.click(toggleNewPeerSection)
peerlistHead.click(togglePeerSection)



