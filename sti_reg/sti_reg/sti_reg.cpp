// sti_reg.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string.h>
#include <Sti.h>
#include <Windows.h>

LPWSTR app_name = L"Scan to shared folder";

int _tmain(int argc, _TCHAR* argv[])
{
	IStillImage* psti;
	HRESULT res = StiCreateInstance(GetModuleHandle(NULL), STI_VERSION, &psti, NULL);
	if (res == S_OK) {
		if (argc == 1 || _tcscmp(argv[1], _T("--deregister")) != 0) {
			res = psti->RegisterLaunchApplication(app_name, L"c:/wifi_scanner/scan.bat");
			if (res == S_OK) {
				printf("Register succeeded\n");
			}
			else {
				printf("Register failed with code %d\n", res);
			}
		}
		else {
			res = psti->UnregisterLaunchApplication(app_name);
			if (res == S_OK) {
				printf("Deregister succeeded\n");
			}
			else {
				printf("Deregister failed with code %d\n", res);
			}
		}
	}
	else {
		printf("Error obtaining IStillImage: %d\n", res);
	}
	return 0;
}

