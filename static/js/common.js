$(function () {
    // 課題5
    $(".delete-btn").click(function () {
        if (confirm("送信してもいいですか？")) {
            return true

        } else {

            return false;
        }
    });
    // 課題7
    $(".delete-account").click(function () {
        if (confirm("本当に削除しますか？")) {
            return true;
        } else {
            return false;
        }
    });
})