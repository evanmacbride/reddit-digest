
# TODO: Use Post class to store attributes from responses. Load Post
# objects into a heapq sorted by postScore. When evaluating Posts to include in
# a snapshot, if a given Post's subreddit is already represented, halve that
# Post's postScore, mark its boolean "halved" property to true, then add the
# Post back to the heapq. Do not halve Posts more than once. If halved is true,
# add the Post to the snapshot without sending it back to the heapq again.
with open(mdFilename,'w',encoding='utf-8') as md:
    md.write("---\ntitle: '" + titleTime + " Snapshot'\ndate: '" + now + "'\n---\n")
    md.write("<ul>\n")
    for resp,sectionTitle,limit in responses:
        postCount = 1
        md.write("<h2>" + sectionTitle + "</h2>" + "\n\n")
        for post in resp.json()['data']['children']:
            if not (post['data']['stickied'] or post['data']['over_18'] or post['data']['spoiler']) and (
                post['data']['url'] not in seenLinks and post['data']['author'] not in seenAuthors):
                postTitle = post['data']['title']
                postUrl = post['data']['url']
                seenLinks.append(post['data']['url'])
                formattedThumbnail = ""
                postThumbnail = ""
                if post['data']['thumbnail'] == "self":
                    postThumbnail = (
    """<svg version='1.1' viewBox='-34 -12 104 64' preserveAspectRatio='xMidYMid slice' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
        <title>text link thumbnail</title>
        <path d='M12.19,8.84a1.45,1.45,0,0,0-1.4-1h-.12a1.46,1.46,0,0,0-1.42,1L1.14,26.56a1.29,1.29,0,0,0-.14.59,1,1,0,0,0,1,1,1.12,1.12,0,0,0,1.08-.77l2.08-4.65h11l2.08,4.59a1.24,1.24,0,0,0,1.12.83,1.08,1.08,0,0,0,1.08-1.08,1.64,1.64,0,0,0-.14-.57ZM6.08,20.71l4.59-10.22,4.6,10.22Z'>
        </path>
        <path d='M32.24,14.78A6.35,6.35,0,0,0,27.6,13.2a11.36,11.36,0,0,0-4.7,1,1,1,0,0,0-.58.89,1,1,0,0,0,.94.92,1.23,1.23,0,0,0,.39-.08,8.87,8.87,0,0,1,3.72-.81c2.7,0,4.28,1.33,4.28,3.92v.5a15.29,15.29,0,0,0-4.42-.61c-3.64,0-6.14,1.61-6.14,4.64v.05c0,2.95,2.7,4.48,5.37,4.48a6.29,6.29,0,0,0,5.19-2.48V26.9a1,1,0,0,0,1,1,1,1,0,0,0,1-1.06V19A5.71,5.71,0,0,0,32.24,14.78Zm-.56,7.7c0,2.28-2.17,3.89-4.81,3.89-1.94,0-3.61-1.06-3.61-2.86v-.06c0-1.8,1.5-3,4.2-3a15.2,15.2,0,0,1,4.22.61Z'>
        </path>
    </svg>""")
                elif post['data']['thumbnail'] in ["","default","image"]:
                    postThumbnail = (
    """<svg version='1.1' viewBox='-34 -14 104 64' preserveAspectRatio='xMidYMid meet' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
        <title>link thumbnail</title>
        <path d='M32,4H4A2,2,0,0,0,2,6V30a2,2,0,0,0,2,2H32a2,2,0,0,0,2-2V6A2,2,0,0,0,32,4ZM4,30V6H32V30Z'></path>
        <path d='M8.92,14a3,3,0,1,0-3-3A3,3,0,0,0,8.92,14Zm0-4.6A1.6,1.6,0,1,1,7.33,11,1.6,1.6,0,0,1,8.92,9.41Z'></path>
        <path d='M22.78,15.37l-5.4,5.4-4-4a1,1,0,0,0-1.41,0L5.92,22.9v2.83l6.79-6.79L16,22.18l-3.75,3.75H15l8.45-8.45L30,24V21.18l-5.81-5.81A1,1,0,0,0,22.78,15.37Z'></path>
    </svg>""")

                else:
                    postThumbnail = "<img src='" + post['data']['thumbnail'] + "' alt='link thumbnail'>"

                formattedThumbnail = "<a href='" + postUrl + "'>" + postThumbnail + "</a>"
                formattedLink = "<div>\n" + "[" + postTitle + "]" + "(" + postUrl + ")\n</div>\n"

                postAuthor = post['data']['author']
                seenAuthors.append(post['data']['author'])
                postComments = str(post['data']['num_comments'])
                postPermalink = post['data']['permalink']
                postCreated = post['data']['created_utc']
                postSubreddit = post['data']['subreddit']
                postScore = str(post['data']['score'])

                thumbnailHTML = ""
                if postThumbnail:
                    thumbnailHTML = (
                        "<a href='" + postUrl + "'>" + postThumbnail + "</a>"
                        )
                linkHTML = "<div class='linkTitle'><a href='" + postUrl + "'>" + postTitle + "</a></div>(" + postUrl.split('/')[2].replace('www.','') + ")"
                infoHTML = (
                        " posted by " + "<a href='https://www.reddit.com/user/" + postAuthor + "'>" + postAuthor + "</a> " +
                        "in " + "<a href='https://www.reddit.com/r/" + postSubreddit + "'>" + postSubreddit + "</a> " +
                        postScore + " points & " + postComments + " <a href='https://www.reddit.com" + postPermalink +"'>comments</a>"
                    )
                linkInfoWrapHTML = (
                    "<div>" +
                        linkHTML + infoHTML +
                    "</div>"
                )
                postHTML = (
                    "<li>" +
                        thumbnailHTML + linkInfoWrapHTML +
                    "</li>"
                )
                md.write(postHTML + "\n\n")
                postCount += 1
                if postCount > limit:
                    break
    md.write("</ul>\n")

md.close()
