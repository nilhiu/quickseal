fileDropArea = document.querySelector("#file-drop-area");
fileDropAreaText = document.querySelector("#file-drop-area-text");
fileDropAreaTextOriginal = fileDropAreaText.innerHTML;
filesInput = document.querySelector("#files-input");

fileDropArea.addEventListener("click", () => {
  filesInput.click();
});

filesInput.addEventListener("change", (e) => {
  if (filesInput.files.length < 1) {
    fileDropAreaText.innerHTML = fileDropAreaTextOriginal;
    return;
  }

  ul = document.createElement("ul");
  for (let i = 0; i < filesInput.files.length; i++) {
    li = document.createElement("li");
    li.innerHTML = filesInput.files[i].name;
    ul.append(li);
  }

  fileDropAreaText.replaceChildren(ul);
});
