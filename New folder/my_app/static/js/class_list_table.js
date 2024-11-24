window.onload = function() {
    var searchFilter = document.getElementById('searchInput')
    var gradeFilter = document.getElementById('gradeFilter');
    var yearFilter = document.getElementById('yearFilter');

    // 監視select和input
    searchFilter.addEventListener('input', filterByGrade);
    gradeFilter.addEventListener('change', filterByGrade);
    yearFilter.addEventListener('change', filterByGrade);


    function filterByGrade() {
        var selected_grade = gradeFilter.value;
        var selected_year = yearFilter.value;
        var value_inputted=searchFilter.value.toLowerCase();

        // 課程資訊
        var rows= document.getElementsByClassName('classes');

        for (var i = rows.length - 1; i >= 0; i--) {
            var titleElement = rows[i].getElementsByClassName('class_title')[0];
            rows[i].classList.remove('not');

            // 确保找到 'class_title' 元素
            if (titleElement) {
                var text = titleElement.innerText.toLowerCase();

                // 根据搜索值过滤元素
                if (text.includes(value_inputted)) {

                }
                else {
                    rows[i].classList.add('not');
                }

            } else {
                // 如果没有找到 'class_title' 元素，则隐藏父元素
                    rows[i].classList.add('not');
            }
        }

        for (var i = rows.length - 1; i >= 0; i--) {
            row=rows[i];
            if (row.classList.contains('not')) {
                row.style.display = 'none';
                continue;
            }

            var grade = row.getElementsByClassName('years_old')[0].innerText.trim();
            var year = row.getElementsByClassName('years')[0].innerText.trim();

            if (selected_grade === 'all' && selected_year === 'all') {
                row.style.display = 'table-row';
            } else if (selected_grade === 'all' && selected_year === year) {
                row.style.display = 'table-row';
            } else if (grade === selected_grade && selected_year === 'all') {
                row.style.display = 'table-row';
            } else if (grade === selected_grade && selected_year === year) {
                row.style.display = 'table-row';
            } else {
                row.style.display = 'none';
            }
        }
    }

}