@echo off
echo Creating QUARXV1 Code Signing Certificate...

REM Create self-signed certificate
makecert -r -pe -n "CN=QUARXV1 ColorBot" -ss CA -sr CurrentUser -a sha256 -cy end -sky signature -sv CA.pvk CA.cer

REM Create code signing certificate
makecert -pe -n "CN=QUARXV1 ColorBot Code Signing" -ss MY -a sha256 -cy end -sky signature -ic CA.cer -iv CA.pvk -sv QUARXV1.pvk QUARXV1.cer

REM Convert to PFX format
pvk2pfx -pvk QUARXV1.pvk -spc QUARXV1.cer -pfx QUARXV1.pfx

echo Certificate created successfully!
echo Files created:
echo   - CA.cer (Certificate Authority)
echo   - CA.pvk (Private Key)
echo   - QUARXV1.cer (Code Signing Certificate)
echo   - QUARXV1.pfx (PFX Certificate)

pause
