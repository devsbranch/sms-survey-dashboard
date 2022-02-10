function setItem(key, value) {
    // Sets cached data about the download the user has requested
    localStorage.setItem(key, JSON.stringify(value));
}

function getItem(key) {
    // Gets cached data about the download the user requested
    const downloadMetaData = JSON.parse(localStorage.getItem(key));
    return downloadMetaData;
}

function removeItem(key) {
    // Clears the cached data about the download the user requested
    localStorage.removeItem(key)
}

function pollAsyncResults(data) {
    // bind pollAsyncResults to itself to avoid clashing with 
    // the prior get request
    // see the URL setup for where this url came from
    const pollAsyncUrl = `${origin}/report/indicators_report/${data.task_id}`

    $.get(pollAsyncUrl)
        .done(function (asyncData, status, xhr) {

            if (asyncData.state === "SUCCESS") {
                // stop making get requests to pollAsyncResults
                removeItem("downloadMetadata")
                clearTimeout(pollAsyncResults);
                $('#download-indicator-report').removeClass('disabled')

                $.notifyBar({ cssClass: "success", html: "Starting Download", delay: 5000 })

                const a = document.createElement('a');
                document.body.appendChild(a);
                a.style = 'display: none';
                a.href = asyncData.download_url;
                a.download = asyncData.filename;

                $('#download-indicator-report').text('Download Indicator Data')
                $('#download-indicator-report').append(' <i class="sl sl-icon-cloud-download ml-2"></i>')
                setTimeout(function () { a.click(); }, 2000)
            }
            // async task still processing
            else if (asyncData.state === "PENDING") {
                // Call the function pollAsyncResults again after 
                // waiting 0.5 seconds.
                setTimeout(function () { pollAsyncResults(data) }, 2000);
            }
            else {
                clearTimeout(pollAsyncResults);
            }
        })
        // see PollAsyncResultsView in View Setup. If the celery 
        // task fails, and returns a JSON blob with status_code 
        // 500, PollAsyncResultsView returns a 500 response, 
        // which would indicate that the task failed
        .fail(function (xhr, status, error) {
            // stop making get requests to pollAsyncResults
            removeItem("downloadMetadata");
            $.notifyBar({ cssClass: "error", html: "An error occured while processing your request", delay: 5000 });
            clearTimeout(pollAsyncResults);

            $('#download-indicator-report').removeClass('buttonload disabled');
            $('#download-indicator-report').removeClass('fa fa-circle-o-notch fa-spin px-2').addClass('mdi mdi-download');
            // add a message, modal, or something to show the user 
            // that there was an error the error in this case 
            // would be related to the asynchronous task's
            // error message
        })
}


$(document).ready(function () {
    const downloadMetaData = getItem("downloadMetadata");

    if (downloadMetaData?.pendingDownload && !downloadMetaData?.downloadStarted) {
        "Your download request is still being processed."
        pollAsyncResults(downloadMetaData)
    }
})


$('#download-indicator-report').on('click', function (e) {
    e.preventDefault();
    const downloadMetaData = getItem("downloadMetadata");
    const projectSlug = $('#download-indicator-report').attr("project-slug")


    if (downloadMetaData?.pendingDownload) {
        $.notifyBar({ cssClass: "warning", html: "Your have already requested this download. Your download will start automatically when ready.", delay: 6000 });

        pollAsyncResults(downloadMetaData)
    } else {
        $.notifyBar({ cssClass: "success", html: "Your download request is being processed. You download will start automatically once the file is ready.", delay: 6000 });
        // see the URL Setup for where this url came from
        const baseUrl = location.origin;
        const url = `${baseUrl}/report/${projectSlug}/indicators_report/`

        $('#download-indicator-report').addClass('disabled').html('Processing');

        $.ajax({ url: url, "credentials": 'include' })
            .done(function (data) {
                setItem("downloadMetadata", { pendingDownload: true, downloadStarted: false, task_id: data.task_id });
                pollAsyncResults(data)
            })

            .fail(function (xhr, status, error) {
                $.notifyBar({ cssClass: "error", html: "An error occured while processing your request", delay: 4000 });
                // add a message, modal, or something to show the user 
                // that there was an error
                // The error in this case would be related to the main 
                // function that makes a request to start the async task
            })
    }
})


