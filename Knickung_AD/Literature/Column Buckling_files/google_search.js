
<!-- =========================== Google Search ============================= -->

function searchWebSite() {
                var searchTerm = document.getElementById("txtSiteSearch").value;
                if (searchTerm != null && searchTerm != "") {
                                var strURL = "https://www.google.com/search";
                                strURL += "?q=" + searchTerm
                                strURL += "+site%3Ahttp%3A%2F%2Fwww.continuummechanics.org&rlz=1C1_____enUS437US437&sugexp=chrome,mod=0&sourceid=chrome&ie=UTF-8"
                                window.open(strURL);
                }
}

