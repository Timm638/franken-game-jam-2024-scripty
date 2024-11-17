{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: {

    devShells.x86_64-linux =
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in
      {
        default = pkgs.mkShell {
          packages = with pkgs; [
            vlc
            libvlc
            python312Full
            python312Packages.pip
          ];
        shellHook = ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.libvlc]}:$LD_LIBRARY_PATH"
          python -m venv .venv
          source .venv/bin/activate
        '';
        };
      };
    };
}
