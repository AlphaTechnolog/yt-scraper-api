{
  description = "A basic api to get youtube videos by applying scraping, made with, python, fast api, selenium and nix.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      lib = pkgs.lib;
      my-python = pkgs.python3.withPackages (ps:
        with ps; [
          fastapi
          uvicorn
          selenium
        ]);
    in {
      devShells.default = pkgs.mkShell {
        name = "youtube-api-dev";
        buildInputs = lib.attrValues {
          inherit (pkgs) geckodriver;
          inherit my-python;
        };
      };
    });
}
