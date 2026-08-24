function addRecommendation() {

    let text = document.getElementById("new-rec").value;

    if (text !== "") {

        let div = document.createElement("div");
        div.className = "rec-card";

        div.innerHTML = "" + text + "";

        document.getElementById("rec-list").appendChild(div);

        alert("Thank you for your recommendation!");

        document.getElementById("new-rec").value = "";
    }

}