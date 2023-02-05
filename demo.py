from infogo import InfoGO

if __name__ == "__main__":
    # ...

    infogo = InfoGO()
    infogo.fed(
        title="Detection Performance of SLEUTH",
        head=["AUC", "Logloss", "ASR", "BA"],
        content=[
            [0.80, 0.12, 0.99, 0.98],
            [0.81, 0.11, 0.97, 0.98],
            [0.88, 0.12, 0.99, 0.99]
        ],
        description="In SLEUTH, encoding and detection are independent on the operation.",
        signature="Jimin"
    )
    infogo.deliver()

    # ...
