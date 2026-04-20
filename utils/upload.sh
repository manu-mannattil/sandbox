#!/usr/bin/env bash
#
# upload.sh -- a script to upload files to various hosts
#
# Updated: Sun, 21 Mar 2021 11:20:20PM -0400
#

# catbox.moe uploader.
catbox() {
    for f
    do
        curl -#q -F "reqtype=fileupload" -F "fileToUpload=@$f" "https://catbox.moe/user/api.php"
    done
}

# Imgur uploader.
# Adapted from: https://gist.github.com/oglops/700373fecf5ffca67f59dfd90f4b9499
imgur() {
    # Scoured from GitHub.
    clientid=$(
        echo -e \
        "1b138bce405b2e0\n" \
        "1d4fa0f8eeeec73\n" \
        "3e7a4deb7ac67da\n" \
        "6bf8cf819aff12a\n" \
        "6c26a0ec0e5496a\n" \
        "85985e0d8fc291d\n" \
        "c7e65b324a5ebe8\n" \
        "c9a6efb3d7932fd\n" \
        "ddc213b38452760\n" \
        "ea6c0ef2987808e\n" \
        shuf              |
        head -n 1
    )

    echo >&2 "${0##*/} (imgur): using client ID: $clientid"

    if [[ $# -gt 1 ]]
    then
        album_response=$(curl -sH "Authorization: Client-ID $clientid" -F "title="  https://api.imgur.com/3/album)
        id=$(echo "$album_response" | grep -P -o '(?<="id":")[^\"]*')
        deletehash=$(echo "$album_response" | grep -P -o '(?<="deletehash":")[^\"]*')
        album_link="http://imgur.com/a/$id"

        for i in "$@"
        do
            image_response="$(curl -# -s -F "image=<$i" -H "Authorization: Client-ID $clientid" -F album=$deletehash -F title="$(basename "$i")" https://api.imgur.com/3/upload.xml)"
            echo >&2 "link: $(grep -P -o '(?<=link>)[^<]*' <<< ${image_response})"
            echo >&2 "delete link: https://imgur.com/delete/$(grep -P -o '(?<=deletehash>)[^<]*' <<< ${image_response})"
            echo >&2 ""
        done

        echo >&2 "album link: $album_link"
        echo >&2 "album deletehash: $deletehash"
    else
        image_response=$(curl -# -F "image"=@"$1" -F title="$(basename "$1")" -H "Authorization: Client-ID $clientid" https://api.imgur.com/3/upload.xml)
        echo >&2 "link: $(grep -P -o '(?<=link>)[^<]*' <<< ${image_response})"
        echo >&2 "delete link: https://imgur.com/delete/$(grep -P -o '(?<=deletehash>)[^<]*' <<< ${image_response})"
    fi
}

# ttm.sh uploader
ttm() {
    for f
    do
        curl -#q -F "file=@$f" "https://ttm.sh"
    done
}

usage="usage: ${0##*/} catbox|imgur|ttm <file>..."

case "$1" in
    catbox|imgur|ttm) cmd="$1"; shift ;;
    *) echo >&2 "$usage"; exit 1 ;;
esac

[[ "$*" ]] || {
    echo >&2 "$usage"
    exit 1
}

"$cmd" "$@"
