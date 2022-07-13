const searchBox = document.getElementById("search-box")
const searchButton = document.getElementById("search-button")
const resultsDiv = document.getElementById("results")


const search = async () => {
    const queryString = searchBox.value
    if (queryString === "") {
        return
    }
    const uri = "/api/v1/search?" + new URLSearchParams({
        q: queryString,
        start: 0
    })

    const response = await fetch(uri)
    const json = await response.json()

    // Update search results UI
    const parent = document.createElement("ol")
    for (const result of json.results) {
        const curNode = document.createElement("li")
        curNode.innerText = result.title
        parent.appendChild(curNode)
    }
    resultsDiv.replaceChildren(parent)
}

searchButton.addEventListener("click", search)
