const searchBox = document.getElementById("search-box");
const resultsBox = document.getElementById("autocomplete-results");

if (searchBox) {
  searchBox.addEventListener("keyup", function () {
    const query = this.value;

    if (query.length < 1) {
      resultsBox.innerHTML = "";
      return;
    }

    fetch(`/search/autocomplete/?q=${query}`)
      .then(res => res.json())
      .then(data => {
        resultsBox.innerHTML = "";

        data.forEach(item => {
          const a = document.createElement("a");
          a.href = `/product/${item.id}/`;
          a.classList.add("list-group-item", "list-group-item-action");
          a.innerText = item.name;

          resultsBox.appendChild(a);
        });
      });
  });
}
