$files = Get-ChildItem -Path .\frontend -Recurse -File -Include *.html,*.js,*.css
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, $utf8NoBom)
    if ($content) {
        $newContent = $content `
            -creplace '>Movies<', '>anime<' `
            -creplace '>DVDs<', '>หนังสือ<' `
            -creplace 'Browse Movies', 'Browse anime' `
            -creplace 'DVDs Available', 'หนังสือ Available' `
            -creplace 'ORDER DVDs ONLINE', 'ORDER หนังสือ ONLINE' `
            -creplace '>Movie<', '>anime<' `
            -creplace 'Back to Movies', 'Back to anime' `
            -creplace 'Available on DVD', 'Available on หนังสือ' `
            -creplace 'No DVDs available', 'No หนังสือ available' `
            -creplace 'Movie not found\.', 'anime not found.' `
            -creplace 'Loading DVDs\.', 'Loading หนังสือ.' `
            -creplace 'No DVDs found\.', 'No หนังสือ found.' `
            -creplace 'Loading Movies\.', 'Loading anime.' `
            -creplace 'No Movies found\.', 'No anime found.' `
            -creplace 'Movies - Animo', 'anime - Animo' `
            -creplace 'Movie - Animo', 'anime - Animo' `
            -creplace 'DVDs - Animo', 'หนังสือ - Animo' `
            -creplace 'Featured Movies', 'Featured anime'
            
        if ($content -cne $newContent) {
            [System.IO.File]::WriteAllText($file.FullName, $newContent, $utf8NoBom)
            Write-Output "Updated $($file.FullName)"
        }
    }
}
